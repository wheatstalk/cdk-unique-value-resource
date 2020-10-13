import { Construct } from '@aws-cdk/core';

import { UniqueValueResourceProps } from './unique-value-resource';
import { UniqueValueResourceBase } from './unique-value-resource-base';

export interface RandomWordsResourceProps extends UniqueValueResourceProps {}

export class UniqueWordsResource extends UniqueValueResourceBase {
  constructor(scope: Construct, id: string, props: RandomWordsResourceProps) {
    super(scope, id, {
      ...props,
      properties: {
        Type: 'UniqueWords',
      },
    });
  }
}
