import argparse
import logging
import time

DEBUG = True

class FileSearcher:
    """
    A class to search for a specific word in a file and log the occurrences.
    """

    def __init__(self, file_path, word, log_level='info', log_file='app.log'):
        """
        Initializes the FileSearcher with the file path, word to search, log level, and log file.
        
        Args:
            file_path (str): The path to the file to be searched.
            word (str): The word to search for in the file.
            log_level (str): The logging level (default is 'info').
            log_file (str): The file to write log messages to (default is 'app.log').
        """
        self.file_path = file_path
        self.word = word
        self.log_file = log_file

        # Set up logging
        self.setup_logging(log_level)

    def setup_logging(self, log_level):
        """
        Sets up the logging configuration.
        
        Args:
            log_level (str): The logging level.
        
        Returns:
            None
        """
        log_level = getattr(logging, log_level.upper(), None)
        if not isinstance(log_level, int):
            raise ValueError(f"Invalid log level: {log_level}")
        
        logging.basicConfig(level=log_level,
                            format="%(asctime)s - %(levelname)s - %(message)s",
                            handlers=[
                                logging.FileHandler(self.log_file),
                                logging.StreamHandler()
                            ])

    def search_word_in_file(self):
        """
        Searches for the specified word in the file and logs the occurrences.
        
        Returns:
            None
        """
        start_time = None
        if DEBUG:
            start_time = time.time()

        occurrences = []
        try:
            with open(self.file_path, 'r') as file:
                for i, line in enumerate(file, 1):
                    if self.word in line:
                        occurrences.append((i, line.strip()))
        except FileNotFoundError:
            logging.error(f"The file {self.file_path} was not found.")
            return
        except Exception as e:
            logging.error(f"An error occurred: {e}")
            return
        
        if occurrences:
            logging.info(f"The word '{self.word}' was found {len(occurrences)} times in the file.")
            for line_num, line in occurrences:
                logging.info(f"Line {line_num}: {line}")
        else:
            logging.info(f"The word '{self.word}' was not found in the file.")

        if start_time is not None:
            elapsed_time = time.time() - start_time
            logging.debug(f"Time taken to search the word: {elapsed_time:.4f} seconds")
            print(f"Time taken to search the word: {elapsed_time:.4f} seconds")
def main():
    """
    Parses command-line arguments and initiates the word search in the specified file.
    
    Command-line Arguments:
        file_path (str): Path to the file to be searched.
        word (str): The word to search for in the file.
        --log (str): Set the logging level (debug, info, warning, error, critical).
        --logfile (str): The file to write log messages to.
        
    Returns:
        None
    """
    parser = argparse.ArgumentParser(description="Search for a word in a file.")
    parser.add_argument('file_path', type=str, help="Path to the file to be searched.")
    parser.add_argument('word', type=str, help="The word to search for in the file.")
    parser.add_argument('--log', type=str, default="info", help="Set the logging level (debug, info, warning, error, critical)")
    parser.add_argument('--logfile', type=str, default="app.log", help="The file to write log messages to.")
    
    args = parser.parse_args()
    
    file_searcher = FileSearcher(args.file_path, args.word, args.log, args.logfile)
    file_searcher.search_word_in_file()

if __name__ == "__main__":
    main()
