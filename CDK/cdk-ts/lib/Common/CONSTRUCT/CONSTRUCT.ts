import { Construct } from 'constructs';
import { STACK } from '../STACK/STACK';

export class CONSTRUCT extends Construct {

    Scope: STACK;

    constructor (scope: STACK)
    {
      super(scope, CONSTRUCT.name + CONSTRUCT.ScopeNext());

      this.Scope = scope;
    }

    private static ScopeCount: number = 0;
    private static ScopeNext(): number {
      CONSTRUCT.ScopeCount++;
      return CONSTRUCT.ScopeCount;
    }

}