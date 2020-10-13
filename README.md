![GitHub Workflow Status](https://img.shields.io/github/workflow/status/wheatstalk/cdk-unique-value-resource/CI-Construct?label=construct%20build)
![GitHub Workflow Status](https://img.shields.io/github/workflow/status/wheatstalk/cdk-unique-value-resource/CI-Lambda?label=lambda%20build)

# CDK Unique Value Resource

This module provides a CloudFormation resource type that produces guaranteed-unique values. You may `!GetAtt` to fetch and use the unique values in your templates. We created this project to help manage dynamic ECS services behind a shared Application Load Balancer.

This project provides AWS CDK Constructs to increase ease of use in your CDK projects. You may install a shared version of the resource provider in a region by using the included CDK app. Or, you may embed and use the provider in your app without any sharing.

Features:

- Create groups of unique values
- Generate unique integers in a given range, with a given step
- Generate UUIDs
- Generate Unique word combinations

## Getting Started

To install a shared version of the resource provider, [install and bootstrap AWS CDK](https://docs.aws.amazon.com/cdk/latest/guide/cli.html), then type the following command:

```bash
cdk --app 'npx @wheatstalk/cdk-unique-value-resource' deploy UniqueValueResource
```

Once this stack has deployed, you may add the dependency to your CDK app:

```bash
# Install with yarn
yarn add @wheatstalk/cdk-unique-value-resource
# Install with npm
npm install @wheatstalk/cdk-unique-value-resource
```

After which, you may start to use it immediately:

```ts
import {
  UniqueValueProvider,
  UniqueIntegerResource,
} from '@wheatstalk/cdk-unique-value-resource';

// Use the shared resource provider.
const provider = UniqueValueProvider.fromRegionalStack(this, 'UniqueValueProvider');

// Create a unique value
const uniqueInteger = new UniqueIntegerResource(this, 'UniqueInteger', {
  provider,
  // Guaranteed uniqueness in the group named 'testing'. You may use a fixed
  // string value as like shown. You may also reference another resource,
  // such as a load balancer listener rule's arn.
  group: 'testing',
  // Start at 10000, inclusive
  start: 10000,
  // Stop at 40000, exclusive
  stop: 40000,
  // Allocate unique numbers
  step: 1,
});

// Display the unique value
new CfnOutput(this, 'UniqueIntegerValue', {
  value: uniqueInteger.uniqueValue,
});
```

## Architecture Notes

- CDK-based project
- Lambda-backed custom resource provider
- Lambda code written in Python
- Allocated values are tracked in a DynamoDB table

## Development Notice

This project is still in development. We do not recommend using it in production until it is stable version `1.0.0`. We do not have nay estimates on when this may be.


## Contributing

We're open to feedback on this project.
