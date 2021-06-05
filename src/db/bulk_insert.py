import logging
import glob
from time import time

from db_utils import get_connexion
from db_utils import execute_sql

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def load_file(path, separator, nb_fields, db_name, sql, chunksize = 5000):
    
    chunk = []
    line_position = 0
    
    for filepath in glob.iglob(path):
        with open(filepath,'r') as file:    
            start = time()
            for line in file:
                line_position += 1
                build_chunk(separator, nb_fields, chunk, line, line_position)

                if (len(chunk) % chunksize == 0):
                    execute_sql(db_name, sql, chunk)
                    del chunk[:]    

        #There is still something to do ...
        if(len(chunk) != 0):
            execute_sql(db_name, sql, chunk) 
        
        #We commit only at the end
        #If there is an error, we dont't load anything
        get_connexion(db_name).commit()

        logging.info(f'Load {filepath} in {time() - start:02f}')

#Build a chunk of lines
#Add line_position as first field on each line
#If number of separator is less than expected, we concatenate with th previous line
#If number of separator is greater than expected, we concatenate inside the last field
def build_chunk(separator, nb_separators, chunk, line, line_position):
    if line.count(separator) < nb_separators:
        logging.debug(f'We concatenate the line {line_position} to the previous one.')
        chunk[-1][nb_separators+1] += line
    elif line.count(separator) > nb_separators:
        split = line.split(separator)
        logging.debug(f'We concatenate the end of line {line_position} inside the last field ({len(split)-nb_separators} inside 1).')
        #Replace the last field with the concatenation (join) - Concise
        split[nb_separators] = separator.join(split[nb_separators:len(split)])
        chunk.append([line_position] + split[0:nb_separators+1])
    else:
        chunk.append([line_position] + line.split(separator)[:])
    return chunk

def main():
    #path = fr'C:\Users\fantv\Desktop\Logs\*.log'
    path = fr'C:\Users\fantv\Desktop\Logs\DRM-WEBAPI-2021-04-07.log'

    sql = "INSERT INTO [control].[WebAPILog_Prod]"\
        " ([LineNumber],[Date],[CorrelationGuid],[ThreadID],[Level],[Logger],[Message])"\
        " VALUES(?,?,?,?,?,?,?)"

    load_file(path, '|', 5, 'DRM_DV1_CTL',sql)
    

if __name__ == "__main__":
    main()