import { Construct } from '@aws-cdk/core';

import { UniqueValueResourceProps } from './unique-value-resource';
import { UniqueValueResourceBase } from './unique-value-resource-base';

export interface UniqueIntegerResourceProps extends UniqueValueResourceProps {
  start: number;
  stop: number;
  step?: number;
}

export class UniqueIntegerResource extends UniqueValueResourceBase {
  constructor(scope: Construct, id: string, props: UniqueIntegerResourceProps) {
    const step = props.step ?? 1;
    const { start, stop } = props;

    if (step === 0) {
      throw new Error('`step` must be non-zero');
    }

    if (start == stop) {
      throw new Error('`start` and `stop` must not be identical');
    }

    if (step > 0 && stop < start) {
      throw new Error('for a positive `step`, `start` must be less than than `stop`');
    }

    if (step < 0 && start < stop) {
      throw new Error('for a negative `step`, `start` must be greater than `stop`');
    }

    super(scope, id, {
      ...props,
      properties: {
        Type: 'UniqueInteger',
        UniqueInteger: {
          Start: start,
          Stop: stop,
          Step: step,
        },
      },
    });
  }
}
