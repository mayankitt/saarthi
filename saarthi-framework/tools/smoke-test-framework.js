#!/usr/bin/env node

const fs = require('fs');
const path = require('path');
const { spawnSync } = require('child_process');

function parseArgs(argv) {
  const args = argv.slice(2);
  let root = process.cwd();
  for (let i = 0; i < args.length; i += 1) {
    const token = args[i];
    if (token === '--root' || token === '-r') {
      root = path.resolve(args[i + 1] || root);
      i += 1;
    }
  }
  return { root };
}

function checkExists(base, relPath) {
  const full = path.join(base, relPath);
  return { relPath, full, ok: fs.existsSync(full) };
}

function printChecks(title, checks) {
  console.log(`\n${title}`);
  checks.forEach((c) => {
    const mark = c.ok ? '[PASS]' : '[FAIL]';
    console.log(`${mark} ${c.relPath} -> ${c.full}`);
  });
}

(function main() {
  const { root } = parseArgs(process.argv);

  const required = [
    'framework.config.yaml',
    '_framework/INDEX.md',
    'tools/validate-work-item.js'
  ];

  const checks = required.map((rel) => checkExists(root, rel));
  printChecks('Smoke test: required files', checks);

  let ok = checks.every((c) => c.ok);

  const validatorPath = path.join(root, 'tools', 'validate-work-item.js');
  if (fs.existsSync(validatorPath)) {
    const result = spawnSync('node', [validatorPath, '--help'], {
      encoding: 'utf8',
      stdio: 'pipe'
    });

    const helpOk = result.status === 0;
    console.log('\nSmoke test: validator executable');
    console.log(`${helpOk ? '[PASS]' : '[FAIL]'} node tools/validate-work-item.js --help`);
    if (!helpOk) {
      if (result.stdout) console.log(result.stdout.trim());
      if (result.stderr) console.log(result.stderr.trim());
    }
    ok = ok && helpOk;
  } else {
    console.log('\nSmoke test: validator executable');
    console.log('[FAIL] validator script not found');
    ok = false;
  }

  console.log(`\n${ok ? 'SMOKE TEST PASSED' : 'SMOKE TEST FAILED'}`);
  process.exit(ok ? 0 : 2);
})();
