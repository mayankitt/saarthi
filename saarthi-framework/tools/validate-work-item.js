#!/usr/bin/env node

const fs = require('fs');
const path = require('path');

function readText(filePath) {
  try {
    return fs.readFileSync(filePath, 'utf8');
  } catch {
    return null;
  }
}

function parseArgs(argv) {
  const args = argv.slice(2);
  let workItemId = null;
  let root = process.cwd();

  for (let i = 0; i < args.length; i += 1) {
    const token = args[i];
    if (token === '--work-item' || token === '-w') {
      workItemId = args[i + 1] || null;
      i += 1;
      continue;
    }
    if (token === '--root' || token === '-r') {
      root = path.resolve(args[i + 1] || root);
      i += 1;
      continue;
    }
    if (token === '--help' || token === '-h') {
      return { help: true };
    }
    if (!token.startsWith('-') && !workItemId) {
      workItemId = token;
    }
  }

  return { workItemId, root, help: false };
}

function usage() {
  return [
    'Usage:',
    '  node tools/validate-work-item.js --work-item <WORK_ITEM_ID> [--root <repoRoot>]',
    '  node tools/validate-work-item.js <WORK_ITEM_ID>',
    '',
    'Exit codes:',
    '  0 = validation passed',
    '  2 = validation failed',
    '  64 = invalid usage'
  ].join('\n');
}

function getSectionLines(mdText, sectionTitle) {
  const lines = mdText.split(/\r?\n/);
  const startRegex = new RegExp(`^##\\s+${sectionTitle.replace(/[.*+?^${}()|[\\]\\]/g, '\\$&')}\\s*$`, 'i');
  let start = -1;
  for (let i = 0; i < lines.length; i += 1) {
    if (startRegex.test(lines[i])) {
      start = i + 1;
      break;
    }
  }
  if (start < 0) {
    return [];
  }

  const result = [];
  for (let i = start; i < lines.length; i += 1) {
    if (/^##\s+/.test(lines[i])) {
      break;
    }
    result.push(lines[i]);
  }
  return result;
}

function extractProfile(summaryText, testPlanText) {
  const fromSummary = /Definition of Done profile:\s*([a-z_]+)\s*-\s*met/i.exec(summaryText);
  if (fromSummary) {
    return fromSummary[1].toLowerCase();
  }

  const fromTestPlan = /Profile \(from framework\.config\.yaml\):\s*([a-z_]+)/i.exec(testPlanText);
  if (fromTestPlan) {
    return fromTestPlan[1].toLowerCase();
  }

  return null;
}

function parseStepsFromConfig(configText) {
  const lines = configText.split(/\r?\n/);
  const steps = [];
  let inSteps = false;

  for (const line of lines) {
    if (!inSteps && /^\s*steps:\s*$/.test(line)) {
      inSteps = true;
      continue;
    }
    if (inSteps) {
      const m = /^\s*-\s*([a-z_]+)\s*$/.exec(line);
      if (m) {
        steps.push(m[1]);
        continue;
      }
      if (/^\s*[a-z_]+:\s*/.test(line)) {
        break;
      }
      if (/^\S/.test(line)) {
        break;
      }
    }
  }

  return steps;
}

function parseProfileRequirements(configText, profileName) {
  const lines = configText.split(/\r?\n/);
  const profileHeader = new RegExp(`^\\s{4}${profileName}:\\s*$`);
  const nextProfileHeader = /^\s{4}[a-z_]+:\s*$/;
  const reqLine = /^\s{6}([a-z_]+):\s*(.+?)\s*(?:#.*)?$/;

  let inProfiles = false;
  let inTarget = false;
  const requirements = {};

  for (const line of lines) {
    if (!inProfiles && /^\s*profiles:\s*$/.test(line)) {
      inProfiles = true;
      continue;
    }

    if (!inProfiles) {
      continue;
    }

    if (!inTarget && profileHeader.test(line)) {
      inTarget = true;
      continue;
    }

    if (inTarget && nextProfileHeader.test(line)) {
      break;
    }

    if (!inTarget) {
      continue;
    }

    const m = reqLine.exec(line);
    if (!m) {
      continue;
    }

    const key = m[1];
    const raw = m[2].trim();
    if (raw === 'true') {
      requirements[key] = true;
    } else if (raw === 'false') {
      requirements[key] = false;
    } else if (raw === 'null') {
      requirements[key] = null;
    } else if (!Number.isNaN(Number(raw))) {
      requirements[key] = Number(raw);
    } else {
      requirements[key] = raw.replace(/^"|"$/g, '');
    }
  }

  return requirements;
}

function parseVerificationCache(cacheText) {
  const lines = cacheText.split(/\r?\n/);
  const commands = {};
  let workItemId = null;
  let discoveredAt = null;
  let inCommands = false;

  for (const line of lines) {
    const idMatch = /^\s*work_item_id:\s*"?([^"#]+)"?/.exec(line);
    if (idMatch) {
      workItemId = idMatch[1].trim();
    }

    const dateMatch = /^\s*discovered_at:\s*"?([^"#]+)"?/.exec(line);
    if (dateMatch) {
      discoveredAt = dateMatch[1].trim();
    }

    if (!inCommands && /^\s*commands:\s*$/.test(line)) {
      inCommands = true;
      continue;
    }

    if (inCommands) {
      const cmd = /^\s{2}([a-z_]+):\s*"?(.*?)"?\s*(?:#.*)?$/.exec(line);
      if (cmd) {
        commands[cmd[1]] = (cmd[2] || '').trim();
        continue;
      }
      if (/^\s*[a-z_]+:\s*/.test(line) && !/^\s{2}[a-z_]+:\s*/.test(line)) {
        break;
      }
    }
  }

  return { workItemId, discoveredAt, commands };
}

function findCoverageDelta(text) {
  const m = /Coverage delta[^:\n]*:\s*[^\d+-]*([+-]?\d+(?:\.\d+)?)/i.exec(text);
  return m ? Number(m[1]) : null;
}

function hasPositiveEvidence(text, patterns, positiveRegex) {
  const lines = text.split(/\r?\n/);
  for (const line of lines) {
    if (patterns.some((p) => p.test(line)) && positiveRegex.test(line)) {
      return true;
    }
  }
  return false;
}

function validateRequirement(key, requiredValue, combinedEvidenceText) {
  if (requiredValue === false || requiredValue === null) {
    return { ok: true, note: `${key} is not required by this profile` };
  }

  const yes = /\b(yes|met|green|clean|pass|passed|approved|0 findings|0 problems|0 failed)\b/i;

  switch (key) {
    case 'build_passes':
      return { ok: hasPositiveEvidence(combinedEvidenceText, [/build/i], yes), note: 'Build evidence present' };
    case 'lint_clean':
      return { ok: hasPositiveEvidence(combinedEvidenceText, [/lint/i], yes), note: 'Lint evidence present' };
    case 'typecheck_clean':
      return { ok: hasPositiveEvidence(combinedEvidenceText, [/typecheck/i], yes), note: 'Typecheck evidence present' };
    case 'new_tests_required': {
      const ok = hasPositiveEvidence(combinedEvidenceText, [/new tests/i], /\b(yes|added|new|pass|passed|green)\b/i)
        || /\(\d+\s+new\)/i.test(combinedEvidenceText);
      return { ok, note: 'New tests evidence present' };
    }
    case 'regression_suite_green':
      return { ok: hasPositiveEvidence(combinedEvidenceText, [/regression/i], yes), note: 'Regression evidence present' };
    case 'no_new_high_severity_findings':
      return {
        ok: hasPositiveEvidence(combinedEvidenceText, [/high-severity findings|high severity findings/i], /\b(yes|none|0)\b/i),
        note: 'High severity findings evidence present'
      };
    case 'self_review_passed':
      return { ok: hasPositiveEvidence(combinedEvidenceText, [/self-review|self review/i], /\b(yes|pass|passed|approved)\b/i), note: 'Self-review evidence present' };
    case 'security_gate_passed':
      return { ok: hasPositiveEvidence(combinedEvidenceText, [/security gate|security recommendation/i], /\b(yes|pass|passed|approved)\b/i), note: 'Security gate evidence present' };
    case 'secret_scan_clean':
      return { ok: hasPositiveEvidence(combinedEvidenceText, [/secret scan/i], /\b(0 findings|clean|yes)\b/i), note: 'Secret scan evidence present' };
    case 'assumptions_documented':
      return { ok: /decision\s*\/\s*assumption register|assumptions?/i.test(combinedEvidenceText), note: 'Assumptions documented' };
    case 'coverage_delta_min_pct': {
      const delta = findCoverageDelta(combinedEvidenceText);
      if (delta === null) {
        return { ok: false, note: `Coverage delta evidence missing (expected >= ${requiredValue})` };
      }
      return { ok: delta >= Number(requiredValue), note: `Coverage delta ${delta} >= ${requiredValue}` };
    }
    default:
      return { ok: true, note: `${key} not currently validated by script` };
  }
}

function printResult(title, items) {
  console.log(`\n${title}`);
  for (const item of items) {
    const mark = item.ok ? '[PASS]' : '[FAIL]';
    console.log(`${mark} ${item.name}: ${item.note}`);
  }
}

(function main() {
  const { workItemId, root, help } = parseArgs(process.argv);

  if (help) {
    console.log(usage());
    process.exit(0);
  }

  if (!workItemId) {
    console.error(usage());
    process.exit(64);
  }

  const repoRoot = root;
  const configPath = path.join(repoRoot, 'framework.config.yaml');
  const itemDir = path.join(repoRoot, 'work-items', workItemId);
  const summaryPath = path.join(itemDir, 'work-item-summary.md');
  const testPlanPath = path.join(itemDir, 'test-plan.md');
  const cachePath = path.join(itemDir, 'verification-commands.yaml');

  const configText = readText(configPath);
  const summaryText = readText(summaryPath);
  const testPlanText = readText(testPlanPath);
  const cacheText = readText(cachePath);

  const fileChecks = [
    { name: 'framework.config.yaml', ok: Boolean(configText), note: configText ? configPath : `Missing ${configPath}` },
    { name: 'work-item-summary.md', ok: Boolean(summaryText), note: summaryText ? summaryPath : `Missing ${summaryPath}` },
    { name: 'test-plan.md', ok: Boolean(testPlanText), note: testPlanText ? testPlanPath : `Missing ${testPlanPath}` },
    { name: 'verification-commands.yaml', ok: Boolean(cacheText), note: cacheText ? cachePath : `Missing ${cachePath}` }
  ];

  printResult('File checks', fileChecks);

  if (fileChecks.some((c) => !c.ok)) {
    process.exit(2);
  }

  const profile = extractProfile(summaryText, testPlanText);
  const profileChecks = [];
  if (!profile) {
    profileChecks.push({ name: 'DoD profile', ok: false, note: 'Could not find DoD profile in summary or test plan' });
    printResult('DoD profile', profileChecks);
    process.exit(2);
  }

  profileChecks.push({ name: 'DoD profile', ok: true, note: `Profile '${profile}' detected` });
  printResult('DoD profile', profileChecks);

  const requirements = parseProfileRequirements(configText, profile);
  if (!Object.keys(requirements).length) {
    console.error(`\n[FAIL] Could not parse requirements for profile '${profile}' from framework.config.yaml`);
    process.exit(2);
  }

  const cache = parseVerificationCache(cacheText);
  const expectedSteps = parseStepsFromConfig(configText);
  const cacheChecks = [];

  cacheChecks.push({
    name: 'cache work_item_id',
    ok: cache.workItemId === workItemId,
    note: cache.workItemId ? `Found '${cache.workItemId}'` : 'Missing work_item_id'
  });

  cacheChecks.push({
    name: 'cache discovered_at',
    ok: Boolean(cache.discoveredAt),
    note: cache.discoveredAt || 'Missing discovered_at'
  });

  for (const step of expectedSteps) {
    cacheChecks.push({
      name: `cache commands.${step}`,
      ok: Object.prototype.hasOwnProperty.call(cache.commands, step),
      note: Object.prototype.hasOwnProperty.call(cache.commands, step)
        ? `Present (${cache.commands[step] ? 'set' : 'empty/not-applicable'})`
        : 'Missing key'
    });
  }

  const hasAtLeastOneCommand = Object.values(cache.commands).some((v) => v && v.length > 0);
  cacheChecks.push({
    name: 'cache has at least one executable command',
    ok: hasAtLeastOneCommand,
    note: hasAtLeastOneCommand ? 'Yes' : 'All commands empty'
  });

  printResult('Verification command cache', cacheChecks);

  const evidenceText = [summaryText, testPlanText].join('\n');
  const reqChecks = [];

  for (const [key, value] of Object.entries(requirements)) {
    const result = validateRequirement(key, value, evidenceText);
    reqChecks.push({ name: key, ok: result.ok, note: result.note });
  }

  printResult(`Definition of Done checks (${profile})`, reqChecks);

  const passed = [...fileChecks, ...profileChecks, ...cacheChecks, ...reqChecks].every((x) => x.ok);

  if (passed) {
    console.log('\nVALIDATION PASSED');
    process.exit(0);
  }

  console.log('\nVALIDATION FAILED');
  process.exit(2);
})();
