import pandas as pd


def get_saramin_loc(directory='') -> pd.DataFrame:
    data = pd.read_csv(f'{directory}saramin_loc.csv')
    data = data.rename(columns={'지역코드': 'saramin_loc'})
    return data.set_index('지역명').to_dict()


def get_saramin_job(directory=''):
    data = pd.read_csv(f'{directory}saramin_job.csv')
    del data['직무 상위 코드']
    del data['직무명']
    data = data.rename(columns={'직무 코드': 'saramin_job'})
    return data.set_index('직무 키워드명').to_dict()
