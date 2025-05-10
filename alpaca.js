const Alpaca = require('@alpacahq/alpaca-trade-api')

const alpaca = new Alpaca({
    keyId: 'PKK94Y8F6NVR86ON60K7',
    secretKey: 'LLzsINCfnW1O3e4K3Rxvhv2tsQQYjFNHo5zjjOpi',
    paper: true,
  })

  console.log(alpaca);

  alpaca.getAccount().then((account) => {
    console.log('Current Account:', account)
  })

//   https://paper-api.alpaca.markets/v2