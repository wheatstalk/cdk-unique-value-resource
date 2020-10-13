import * as cdk from '@aws-cdk/core';

import { IUniqueValueResource, UniqueValueResourceProps } from './unique-value-resource';

export interface UniqueValueResourceBaseProps extends UniqueValueResourceProps {
  properties: Record<string, unknown>;
}

export class UniqueValueResourceBase extends cdk.CustomResource implements IUniqueValueResource {
  public readonly uniqueValue: string;

  constructor(scope: cdk.Construct, id: string, props: UniqueValueResourceBaseProps) {
    super(scope, id, {
      serviceToken: props.provider.serviceToken,
      properties: {
        Group: props.group,
        ...props.properties,
      },
    });

    this.uniqueValue = this.getAttString('UniqueValue');
  }
}
