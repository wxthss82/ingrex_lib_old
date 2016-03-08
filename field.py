from ingrex import Intel, Utils

import sys
default_encoding = 'utf-8'
if sys.getdefaultencoding() != default_encoding:
    reload(sys)

    sys.setdefaultencoding(default_encoding)

def main():
    "main function"
    field = {
        # 'minLngE6':116298171,
        # 'minLatE6':39986831,
        # 'maxLngE6':116311303,
        # 'maxLatE6':39990941,
        'minLngE6':115523545,
        'minLatE6':39418597,
        'maxLngE6':117005055,
        'maxLatE6':40404834,
    }
    with open('cookies') as cookies:
        cookies = cookies.read().strip()

    minxtile, maxytile = Utils.calc_tile(field['minLngE6']/1E6, field['minLatE6']/1E6, 15)
    maxxtile, minytile = Utils.calc_tile(field['maxLngE6']/1E6, field['maxLatE6']/1E6, 15)
    for xtile in range(minxtile, maxxtile + 1):
        for ytile in range(minytile, maxytile + 1):
            tilekey = '15_{}_{}_8_8_25'.format(xtile, ytile)
            intel = Intel(cookies, field)
            result = intel.fetch_map([tilekey])
            entities = result['map'][tilekey]['gameEntities']
            for entity in entities:
                if entity[0].endswith('.16'):
                    print(entity)
                    with open("portal.txt", "a") as myfile:
                        myfile.write(entity[0] + "\t" + str(entity[1]) + "\t" + entity[2][0] + "\t" + entity[2][1] + "\t" + str(entity[2][2]) + "\t" + str(entity[2][3]) + "\t" + entity[2][7] + "\t" + entity[2][8].encode('utf-8'))
                        myfile.write("\n")
                if entity[0].endswith('.9'):
                    print(entity)
                    with open("field.txt", "a") as myfile:
                        myfile.write(entity[0] + "\t" + str(entity[1]) + "\t" + entity[2][0] + "\t" + entity[2][1] + "\t" + entity[2][2] + "\t" + str(entity[2][3]) + "\t" + str(entity[2][4]) + "\t" + entity[2][5] + "\t" + str(entity[2][6]) + "\t" + str(entity[2][7]))
                        myfile.write("\n")

if __name__ == '__main__':
    main()
