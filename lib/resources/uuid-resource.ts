import { Construct } from '@aws-cdk/core';

import { UniqueValueResourceProps } from './unique-value-resource';
import { UniqueValueResourceBase } from './unique-value-resource-base';

export interface UUIDResourceProps extends UniqueValueResourceProps {}

export class UUIDResource extends UniqueValueResourceBase {
  constructor(scope: Construct, id: string, props: UUIDResourceProps) {
    super(scope, id, {
      ...props,
      properties: {
        Type: 'UUID',
      },
    });
  }
}
