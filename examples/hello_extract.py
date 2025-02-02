from dataclasses import dataclass

import vexora


@dataclass
class Currency:
    name: str
    symbol: str


if __name__ == "__main__":
    print(
        vexora.extract(
            "After flying ORD to Heathrow, I exchanged my greenbacks for local currency.",
            target=Currency,
        ),
    )
"""
» python examples/hello_extract.py
╭─ vexora ─────────────────────────────────────────────────────────────────────────────────────────╮
│ ⠋   Final Result                                                                                 │
│     Input:   {                                                                                   │
│                'response': {                                                                     │
│                  'task_id': '32669832-4ebc-482f-bcda-dbd2a5f2ea3d',                              │
│                  'result': [                                                                     │
│                    {                                                                             │
│                      'name': 'US Dollar',                                                        │
│                      'symbol': 'USD'                                                             │
│                    },                                                                            │
│                    {                                                                             │
│                      'name': 'British Pound Sterling',                                           │
│                      'symbol': 'GBP'                                                             │
│                    }                                                                             │
│                  ]                                                                               │
│                }                                                                                 │
│              }                                                                                   │
╰──────────────────────────────────────────────────────────────────────────────────── 11:45:43 PM ─╯
[Currency(name='US Dollar', symbol='USD'), Currency(name='British Pound Sterling', symbol='GBP')]
"""
