import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableRow,
} from '@mui/material';

export type PredictionTableProps = {
  columns: string[];
  predictions: Record<string, number>;
};

/**
 * A table containing predicted genres and their confidence values. Sorted in
 * descending order by confidence value by default.
 *
 * @see https://mui.com/material-ui/react-table/#EnhancedTable.tsx which inspired this component
 */
export const PredictionTable = (props: PredictionTableProps) => {
  const { columns, predictions } = props;
  return (
    <Table size="small">
      <PredictionTableHeader columns={columns} />
      <PredictionTableBody predictions={predictions} />
    </Table>
  );
};

/**
 * Table header with columns labels mapped from the passed `columns` prop
*/
const PredictionTableHeader = ({ columns }: Pick<PredictionTableProps, 'columns'>) => {
  return (
    <TableHead>
      <TableRow>
        { columns.map(column => <TableCell key={column.toLowerCase()}>{column}</TableCell>) }
      </TableRow>
    </TableHead>
  );
};

/**
 * Table body with predicted genres and their confidence values, with rows sorted in descending
 * order by confidence value.
 */
const PredictionTableBody = ({ predictions }: Pick<PredictionTableProps, 'predictions'>) => {
  const predictionsArray = Object.entries(predictions).sort((firstEntry, secondEntry) => {
    return secondEntry[1] - firstEntry[1];  // by confidence value in descending order
  });

  return (
    <TableBody>
      { predictionsArray.map(([genre, confidence]) => (
        <TableRow key={genre}>
          <TableCell sx={{ textTransform: 'capitalize' }}>{ genre }</TableCell>
          <TableCell align="right">{ `${(100 * confidence).toFixed(3)}%` }</TableCell>
        </TableRow>
      ))}
    </TableBody>
  );
};
