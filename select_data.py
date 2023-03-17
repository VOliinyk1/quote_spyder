import connect
from models import Quotes, Authors

def parse_input(inp: str) -> list:
    command_args = inp.split(':')
    return command_args[0], command_args[1] 
    

def find_by_name(*args):
    result = ''
    author_obj = Authors.objects(fullname=args[0])[0]
    quotes = Quotes.objects(author=author_obj.id)
    
    for qt in quotes:
        
        tags = [tag for tag in qt.tags]
        author_name = qt.author.fullname
        
        result += f'id: {qt.id} author name: {author_name} quote: {qt.quote} tags :{tags}\n\n'
    return result

def find_by_one_tag(*args):
    result = ''
    
    quotes = Quotes.objects(tags = args[0])
    
    for qt in quotes:
        
        tags = [tag for tag in qt.tags]
        author_name = qt.author.fullname
        
        result += f'id: {qt.id} author name: {author_name} quote: {qt.quote} tags:{tags}\n\n'
    return result

def find_by_many_tags(*args):
    result = ''
    tags_list = list(args)[0].split(',')
    quotes = []
    for tag in tags_list:
        quotes.append(Quotes.objects(tags=tag)[0])

    for qt in quotes:
        
        tags = [tag for tag in qt.tags]
        author_name = qt.author.fullname
        
        result += f'id: {qt.id} author name: {author_name} quote: {qt.quote} tags:{tags}\n\n'
    return result

COMMANDS = {'name': find_by_name,
            'tag': find_by_one_tag,
            'tags': find_by_many_tags}
inp = input('> ')

while inp != 'exit':
    command, args = parse_input(inp)
    print(COMMANDS[command](args))
    inp = input('> ')