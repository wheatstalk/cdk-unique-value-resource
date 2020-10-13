import * as cdk from '@aws-cdk/core';
import { Construct } from '@aws-cdk/core';

import { UniqueValueResourceProvider } from './provider';
import { UniqueIntegerResource, UniqueWordsResource, UUIDResource } from './resources';

export class TestResourcesStack extends cdk.Stack {
  constructor(scope: Construct, id: string, props?: cdk.StackProps) {
    super(scope, id, props);

    const provider = UniqueValueResourceProvider.fromRegionalStack(this, 'Provider');

    const uniqueInteger = new UniqueIntegerResource(this, 'UniqueInteger', {
      provider,
      group: this.stackName,
      start: 1000,
      stop: 10000,
    });

    new cdk.CfnOutput(this, 'UniqueIntegerValue', {
      value: uniqueInteger.uniqueValue,
    });

    const randomWords = new UniqueWordsResource(this, 'UniqueWords', {
      provider,
      group: this.stackName,
    });

    new cdk.CfnOutput(this, 'UniqueWordsValue', {
      value: randomWords.uniqueValue,
    });

    const uuid = new UUIDResource(this, 'UUID', {
      provider,
      group: this.stackName,
    });

    new cdk.CfnOutput(this, 'UUIDValue', {
      value: uuid.uniqueValue,
    });
  }
}
