import { formatDate } from '@angular/common';
import { Color } from 'ng2-charts';
import { Coin, CoinDetail, CurrentPrices, FormattedCurrentPrice } from '../models/coin.model';
import { TableChart } from '../models/chart.model'

export function toFixed(x: any) {
  // convert numbers in scientific / exp format to fixed point number strings
  // Shamelessly stolen from here:
  // https://stackoverflow.com/questions/1685680/how-to-avoid-scientific-notation-for-large-numbers-in-javascript
  if (Math.abs(x) < 1.0) {
    var e = parseInt(x.toString().split('e-')[1]);
    if (e) {
      x *= Math.pow(10, e - 1);
      x = '0.' + (new Array(e)).join('0') + x.toString().substring(2);
    }
  } else {
    var e = parseInt(x.toString().split('+')[1]);
    if (e > 20) {
      e -= 20;
      x /= Math.pow(10, e);
      x += (new Array(e + 1)).join('0');
    }
  }
  return x;
}

export function roundToString(num: number, dp: number) {
  // We have to deal with very large and very small numbers
  // here we add some logic to try to deal with the edge cases
  // ie btc: 50,000.00 to shib 0.000027
  let multiple: number = dp * 10
  let rounded: number = Math.round(num * multiple) / multiple
  // necessary to avoid JS exponential number representations
  // yikes
  if (rounded == 0 && num < 0.001 && num > 0) {
    // very small numbers
    return toFixed(num)
  }
  else if (rounded == 0) {
    // round to specified dps
    return num.toPrecision(dp)
  }
  else {
    // just strinify
    return rounded.toString()
  }
}

export function formatCurrentPrice(currentPrice: CurrentPrices) {
  // format a list of current prices
  // these are returned from api on coin list and detail views
  let percentageChange = 100 - (currentPrice.rate_open / currentPrice.rate_close) * 100
  let change = roundToString(percentageChange, 2)

  let fcp: FormattedCurrentPrice = {
    change: `${change}%`,
    current: roundToString(currentPrice.rate_close, 2),
    date: currentPrice.time_period_end
  }
  return fcp
};

export function formatCoinHistory(coin: Coin | CoinDetail) {
  // convert coin history to a human readable format
  let labels: any[] = [];
  let points: any[] = [];

  // loop on all data points, converting dates
  for (let pricePoint of coin.coinprices_set) {
    labels.push(formatDate(pricePoint.time_close, 'Y-M-d', 'en-us'))
    points.push(pricePoint.rate_close)
  }

  // get color red (fall) or green (rise) from price 
  let color: Color[] = getColor(points)

  // add to typed object
  let tc: TableChart = {
    data: [{ data: points, label: 'Series A' },],
    labels: labels,
    color: color
  }
  return tc
}

export function getColor(points: number[]) {
  // get color red (fall) or green (rise) from price 
  let color: Color[];
  if (points[0] > points[points.length - 1]) {
    // red, as prices decreased
    color = [
      {
        borderColor: 'rgba(255,0,0,0.3)',
        backgroundColor: 'rgba(255,0,0,0.3)',
      },
    ]
  }
  else {
    // green, as prices increased
    color = [
      {
        borderColor: 'rgba(0,255,0,0.3)',
        backgroundColor: 'rgba(0,255,0,0.3)',
      },
    ]
  }
  return color
}
