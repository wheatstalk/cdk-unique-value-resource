import { IUniqueValueResourceProvider } from '../provider';

export interface IUniqueValueResource {
  readonly uniqueValue: string;
}

export interface UniqueValueResourceProps {
  provider: IUniqueValueResourceProvider;
  group: string;
}
