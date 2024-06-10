from TxtToCsv import TxtToCsv

def main():
    converter = TxtToCsv('./logs_txt/')
    converter.process()
    
    print(converter.data.head(5))

if __name__ == '__main__':
    main()