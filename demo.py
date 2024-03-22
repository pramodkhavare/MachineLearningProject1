from Housing.src.pipeline.training_pipeline import Pipeline 
from Housing.src.exception import HousingException
from Housing.src.logger import logging

def main():
    try:
        pipeline = Pipeline()
        pipeline.run_pipeline() 

    except Exception as e:
        logging.error(f"{e}")
        print(e)

if __name__ == "__main__":
    main()