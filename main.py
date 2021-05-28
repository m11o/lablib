import fluorine.constant as const
import fluorine.separate_timings as st

if __name__ == "__main__":
    for animal in const.ANIMAL_NUMBERS:
        file_path = "./resources/ID181106Cre/ID181106Cre%s_Processed/ID181106Cre%s_Longitudinal_Traces.csv" % (animal, animal)
        separate_timing_instance = st.SeparateTiming(file_path)
        separate_timing_instance.exec()
