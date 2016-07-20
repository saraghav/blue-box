function csvdata = read_csv_with_headers(file)

headers = get_csv_headers(file);

row_offset = 1; % skip header
col_offset = 0;
data = csvread(file, row_offset, col_offset); %#ok<NASGU>

csvdata = struct;

for i=1:1:length(headers)
    header = headers(i);
    cmd_array = ['csvdata.' header ' = ' 'data(:,', int2str(i), ');'];
    cmd = strjoin(cmd_array, '');
    disp(cmd);
    eval(cmd);
end