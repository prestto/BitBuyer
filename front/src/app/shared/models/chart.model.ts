import { Color, Label } from 'ng2-charts';
import { ChartDataSets } from 'chart.js';

export interface TableChart {
  data: ChartDataSets[];
  labels: Label[];
  color: Color[];
}
