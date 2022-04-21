import csv

with open('dataset.csv', newline='') as f:
    reader = csv.reader(f)
    x = []
    for i in f:
        x.append(i.strip().split('\t'))

result = []
for i in x:
    x = i[-1]
    main = i[:-1]
    if len(i) < 6:
        continue
    else:
        g = x.replace('(', '', 100).replace(')', '', 100).replace('-', '', 100)
        if '+380' in g:
            t = (list(filter(lambda y: '+380' in y, g.split())))
            if len(t) > 0:
                res = (t[0][1:-1])
                main.append(res)
    if '@' in x:
        t2 = (list(filter(lambda y: '@' in y, x.split())))
        main += t2
    if 'www' in x:
        t3 = (list(filter(lambda y: 'www' in y, x.split())))
        main += t3
    result.append(main)

with open('dataset_fixed.csv', 'w') as f2:
    csv_writer = csv.writer(f2, delimiter='\t')
    for i in result:
        csv_writer.writerow(i)


















