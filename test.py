#!python2

print('hello wotld')
import gamelib

def main():
    mymap = gamelib.TF2()

    with open('demofile', 'w') as demofile:
        demofile.write(str(mymap))

if __name__ == '__main__':
    main()
