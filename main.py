from TourGuide import TourGuide
import pandas as pd

if __name__ == "__main__":
    data = pd.read_csv('data.txt', sep=";", header=0, decimal=',')
    
    ourPathGuide = TourGuide(data)
    ourPathGuide.build_route()
    ourPathGuide.set_overall_time(24)
    ourPathGuide.build_route()
