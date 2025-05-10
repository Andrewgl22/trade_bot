const Alpaca = require('@alpacahq/alpaca-trade-api')

const alpaca = new Alpaca({
    keyId: '',
    secretKey: '',
    paper: true,
  })

  console.log(alpaca);

  alpaca.getAccount().then((account) => {
    console.log('Current Account:', account)
  })

//   https://paper-api.alpaca.markets/v2