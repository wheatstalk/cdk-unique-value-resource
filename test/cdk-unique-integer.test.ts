import { expect as expectCDK, MatchStyle, matchTemplate } from '@aws-cdk/assert';
import * as cdk from '@aws-cdk/core';

import { DiagnosticStack } from '../lib/diagnostic-stack';

test('Empty Stack', () => {
  const app = new cdk.App();
  // WHEN
  const stack = new DiagnosticStack(app, 'MyTestStack');
  // THEN
  expectCDK(stack).to(
    matchTemplate(
      {
        Resources: {},
      },
      MatchStyle.EXACT,
    ),
  );
});
