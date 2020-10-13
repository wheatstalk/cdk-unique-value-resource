import * as cdk from '@aws-cdk/core';
import { Construct } from '@aws-cdk/core';

import { UniqueValueResourceProvider } from './provider';
import { UniqueIntegerResource, UniqueWordsResource, UUIDResource } from './resources';

export class DiagnosticStack extends cdk.Stack {
  constructor(scope: Construct, id: string, props?: cdk.StackProps) {
    super(scope, id, props);

    const provider = new UniqueValueResourceProvider(this, 'Provider');

    new cdk.CfnOutput(this, 'ServiceToken', {
      value: provider.serviceToken,
    });

    this.manyUniqueIntegerResources(provider, 10);
    this.manyUuidResources(provider, 10);
    this.manyRandomWordResources(provider, 10);
  }

  private manyUuidResources(provider: UniqueValueResourceProvider, count: number) {
    for (let i = 0; i < count; i++) {
      const group = getRandomGroup();
      const uuidResource = new UUIDResource(this, `UUID${group}${i}`, {
        provider,
        group: group,
      });

      new cdk.CfnOutput(this, `UUID${group}${i}Value`, {
        value: uuidResource.uniqueValue,
      });
    }
  }

  private manyUniqueIntegerResources(provider: UniqueValueResourceProvider, count: number) {
    for (let i = 0; i < count; i++) {
      const group = getRandomGroup();
      const resource = new UniqueIntegerResource(this, `Int${group}${i}`, {
        provider,
        group: group,
        start: 1000,
        stop: 10000,
      });

      new cdk.CfnOutput(this, `Int${group}${i}Value`, {
        value: resource.uniqueValue,
      });
    }
  }

  private manyRandomWordResources(provider: UniqueValueResourceProvider, count: number) {
    for (let i = 0; i < count; i++) {
      const group = getRandomGroup();
      const resource = new UniqueWordsResource(this, `RandomWords${group}${i}`, {
        provider,
        group: group,
      });

      new cdk.CfnOutput(this, `RandomWords${group}${i}Value`, {
        value: resource.uniqueValue,
      });
    }
  }
}

function getRandomGroup() {
  const groups = ['A', 'B'];
  return groups[Math.floor(Math.random() * groups.length)];
}
