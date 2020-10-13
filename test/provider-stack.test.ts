import { expect as expectCDK, haveOutput, haveResourceLike, MatchStyle, matchTemplate } from '@aws-cdk/assert';
import * as cdk from '@aws-cdk/core';

import { ProviderStack } from '../lib/provider-stack';

test('provider stack has service service token export', () => {
  const app = new cdk.App();
  // WHEN
  const stack = new ProviderStack(app, 'UniqueValueProvider');
  // THEN
  expectCDK(stack).to(
    haveOutput({
      exportName: 'UniqueValueProvider-ServiceToken',
    }),
  );
});

test('no replacement or deletion of records table', () => {
  const app = new cdk.App();
  // WHEN
  const stack = new ProviderStack(app, 'UniqueValueProvider');
  // THEN
  expectCDK(stack).to(haveResourceLike('AWS::DynamoDB::Table'));
  expectCDK(stack).to(
    matchTemplate(
      {
        Resources: {
          ProviderRecordsEDE8495D: {
            Type: 'AWS::DynamoDB::Table',
            Properties: {
              KeySchema: [
                {
                  AttributeName: 'group',
                  KeyType: 'HASH',
                },
              ],
              AttributeDefinitions: [
                {
                  AttributeName: 'group',
                  AttributeType: 'S',
                },
              ],
            },
          },
        },
      },
      MatchStyle.NO_REPLACES,
    ),
  );
});
