import * as cdk from '@aws-cdk/core';
import { Construct } from '@aws-cdk/core';

import { UniqueValueResourceProvider } from './provider';

export class ProviderStack extends cdk.Stack {
  constructor(scope: Construct, id: string, props?: cdk.StackProps) {
    super(scope, id, props);

    const provider = new UniqueValueResourceProvider(this, 'Provider');

    new cdk.CfnOutput(this, 'ServiceToken', {
      value: provider.serviceToken,
      exportName: cdk.Fn.join('-', [this.stackName, 'ServiceToken']),
    });
  }
}
