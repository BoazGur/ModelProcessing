from Parser import Parser

def main():
    converter = Parser('./logs_txt/')
    converter.process()
    converter.to_xes('final.csv')
    
    disocverer = Disocverer('final.csv')

if __name__ == '__main__':
    main()