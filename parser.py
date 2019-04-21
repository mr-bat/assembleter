while True:
    a = raw_input().split('//--')
    print(a[1].split('//')[0].lstrip())
