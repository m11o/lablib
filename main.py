import utils.constant as const
import fluorine.separate_timings as st

import fluorine.insert_data as idata

if __name__ == "__main__":
    for animal in const.ANIMAL_NUMBERS:
        animal_name = 'ID181106Cre%s' % animal

        # separate_timing_instance = st.SeparateTiming(file_path)
        # separate_timing_instance.exec()

        idata.InsertData(animal_name, 'ID181106Cre').exec()
