# Swarm

## Hello World

```
define hello:
    init:
        "Hello World!" -> print
```
```
Hello World!
```

## Conceptual structure

The design of **Swarm** is meant to emulate the design paradigm of microservice architecture on a smaller scale (think one server instance rather than many). To that end, the overall structure is analogous to a set of distinct processes that communicate via HTTP-style requests. These pseudo-processes are called 'agents', and the requests are handled via the 'send' command (`->`).

## Design goals

- Handles HTTP requests easily "out of the box"
- Excels as a server talking to many APIs
- Easy multiprocessing and flexible scaling
- Powerful and efficient HTML generation

## Philosophy

- Language design should encourage good program design
- If possible, don't reinvent the wheel. People already know how to use wheels.
- Prioritize legibility. Code is written once. It's read many times, usually by people unfamiliar with it (even your own future self!)
- Be just clever enough
- Less is more

## Language Vision

- A single file can be run locally, deployed to a single cloud server, or auto-deployed to a set of servers, by only changing a few options. (This seems most easily doable by having a deployment manager that reads the code, either asks the user or reads a brief deployment config file, and deploys it in the desired fashion. Presumably transpiling will be required (Go seems a good target), potentially rewriting one source file into many, for many distinct services, while keeping all the links of flow intact)
- A single file (or several files with imports, if it aids human conceptualization) can describe an entire composite of microservices
- Templates that are easy to write and easy to read make specifying the communication between microservices as easy as possible

## To Do

- [x] Document language vision and philosophy
- [ ] Complete working interpreter
- [ ] Document all implemented functionality
- [ ] Complete optimized working/interpreter











## HTML generation

Swarm is designed to make HTML generation as easy as possible:

```
listItems = ['apple','pear','orange','banana']

html = '''
<!DOCTYPE html>
<html>
<head>
<title><<<title>>></title>
</head>
<body>
{{{body}}}
</body>
</html>
'''

body = '<ul>'
for i in listItems:
    body += '<li>{item}</li>'.replace('{item}',i)
body += '</ul>'

html.replace((('{{{body}}}',body),
              ('<<<title>>>','Fruit: A Primer')))

html.human
html -> print
```
```
<!DOCTYPE html>
<html>
  <head>
    <title>Fruit: A Primer</title>
  </head>
  <body>
    <ul>
      <li>apple</li>
      <li>pear</li>
      <li>orange</li>
      <li>banana</li>
    </ul>
  </body>
</html>
```
Note that no particular syntax is required to denote where to replace, ie `<<<title>>>` and `{{{body}}}` both worked fine. Anything you can specify via regex, you can replace. The replacement happens one pair at a time, over the entire document:
```
s = 'aab'
s.replace([['ab', 'aab'],
           ['aab','aa']])
s -> print
s = 'aab'
s.replace([['aab','aa'],
           ['ab', 'aab']])
s -> print
```
```
aaa
aa
```
```
s = 'a'
s.replace([['a','ac'],
           ['a','ab'],
           ['c','cd']])
s -> print
```
```
abcd
```

Let's try a somewhat more complex HTML generation example:

```
define records:
    init:
        status1 = {'Service X':'green',
                   'Service Y':'green',
                   'Service Z':'green'}
        status2 = {'Service I':'green',
                   'Service J':'red',
                   'Service K':'green'}

    run(ip):
        ip,{'Status: Group 1':status1,'Status: Group 2':status2} -> build

define build(ip,data):
        template = '''
        <!DOCTYPE html>
        <html>
          <head>
            <title>{{{title}}}</title>
          </head>
          <body>
            {{{body}}}
          </body>
        </html>
        '''

        body = ''
        for group,elem in data:
            body += '<h2>{{{group}}}</h2>'.replace('{{{group}}}',group)

            body += '<p><ul>'
            for service,status in elem:
                body += '<li style="color:{{{status}}}">{{{service}}}</li>'.replace((('{{{service}}}',service),
                                                                                     ('{{{status}}}',status)))
            body += '</ul></p>'

        template.replace((('{{{title}}}','STATUS REPORT'),
                          ('{{{body}}}',body)))

        template.human
        template -> HTTP.send(ip)
```


```
<!DOCTYPE html>
<html>
  <head>
    <title>STATUS REPORT</title>
  </head>
  <body>
    <h2>Status: Group 1</h2>
    <p>
      <ul>
        <li style="color:green">Service X</li>
        <li style="color:green">Service Y</li>
        <li style="color:green">Service Z</li>
      </ul>
    </p>
    <h2>Status: Group 2</h2>
    <p>
      <ul>
        <li style="color:green">Service I</li>
        <li style="color:red">Service J</li>
        <li style="color:green">Service K</li>
      </ul>
    </p>
  </body>
</html>

```

Regexes with or without capture groups are also valid arguments to pass to `.replace`. For example, the following will remove all bold tags from a string, while leaving their contents unchanged.
```
someBigString.replace(((r'<b>(.*?)</b>',r'\1')))
```
This command will bold all instances of 'Swarm' or 'swarm', and italic all instances of 'Agent', 'Agents', 'agent', or 'agents':
```
someBigString.replace(((r'([Ss]warm)',r'<b>\1</b>'),
                       (r'([Aa]gent[s]?)',r'<i>\1</i>')))
```


# Further Examples

- [Basic Patterns](docs/examples.md)
- [Simple Project Euler Solutions](docs/project_euler.md)
- [Language Specification](docs/specification.md)
