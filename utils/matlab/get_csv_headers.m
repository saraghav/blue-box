function headers = get_csv_headers(file)

fileID = fopen(file, 'r');
formatspec = '%s';
header_row = textscan(fileID, formatspec, 1);
fclose(fileID);
delimiter = ',';
headers = strsplit(header_row{1}{1}, delimiter);