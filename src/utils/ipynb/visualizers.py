class DataFrameVisualizer:
    """
    """
    @staticmethod
    def default_view(data):
        print(f'{data.head()}')

    @staticmethod
    def type_view(data):
        print(f'{data.head()}')
        print(f'\nDataset - Data Types:\n{data.dtypes}')

    view_options = {
        'default': default_view,
        'type': type_view}

    @classmethod
    def choice_validate(cls, choice):
        return choice if choice in cls.view_options else 'default'

    @classmethod
    def viewer(cls, data, view_choice='default'):
        choice = cls.choice_validate(view_choice)

        def view_data(data):
            print(f'Dataset - Preview:')
            cls.view_options[choice](data)

        if hasattr(data, '__dataframe__'):
            view_data(data)
        elif isinstance(data, list):
            for i, df in enumerate(data):
                print(f'Dataset {i} - Preview:')
                view_data(df)
        
        print('\n' + '-' * 56 + '\n')