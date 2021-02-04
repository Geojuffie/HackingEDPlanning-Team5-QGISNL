from math import floor


_multipliers = {
    0: [
        [0.3616, -0.2768, 0.1488, -0.0336, 0.0000],
        [0.2640, -0.0960, 0.0400, -0.0080, 0.0000],
        [0.1840, 0.0400, -0.0320, 0.0080, 0.0000],
        [0.1200, 0.1360, -0.0720, 0.0160, 0.0000],
        [0.0704, 0.1968, -0.0848, 0.0176, 0.0000]
    ],
    5: [
        [0.0336, 0.2272, -0.0752, 0.0144, 0.0000],
        [0.0080, 0.2320, -0.0480, 0.0080, 0.0000],
        [-0.0080, 0.2160, -0.0080, 0.0000, 0.0000],
        [-0.0160, 0.1840, 0.0400, -0.0080, 0.0000],
        [-0.0176, 0.1408, 0.0912, -0.0144, 0.0000]
    ],
    10: [
        [-0.0128, 0.0848, 0.1504, -0.0240, 0.0016],
        [-0.0016, 0.0144, 0.2224, -0.0416, 0.0064],
        [0.0064, -0.0336, 0.2544, -0.0336, 0.0064],
        [0.0064, -0.0416, 0.2224, 0.0144, -0.0016],
        [0.0016, -0.0240, 0.1504, 0.0848, -0.0128]
    ],
    70: [
        [-0.0144, 0.0912, 0.1408, -0.0176, 0.0000],
        [-0.0080, 0.0400, 0.1840, -0.0160, 0.0000],
        [0.0000, -0.0080, 0.2160, -0.0080, 0.0000],
        [0.0080, -0.0480, 0.2320, 0.0080, 0.0000],
        [0.0144, -0.0752, 0.2272, 0.0336, 0.0000]
    ],
    75: [
        [0.0176, -0.0848, 0.1968, 0.0704, 0.0000],
        [0.0160, -0.0720, 0.1360, 0.1200, 0.0000],
        [0.0080, -0.0320, 0.0400, 0.1840, 0.0000],
        [-0.0080, 0.0400, -0.0960, 0.2640, 0.0000],
        [-0.0336, 0.1488, -0.2768, 0.3616, 0.0000]
    ]
}



class Sprague():

    def __init__(self):
        self.ages = {}


    def __str__(self):
        result = 'Sprague[len: {len(self.ages)}]'
        return result


    def _get_multipliers_panel_and_n(self, age):
        panel_key = -1
        for key in _multipliers:
            #print(k)
            if key <= age and key > panel_key:
                panel_key = key
        n = age % 5
        return (panel_key, n)


    def _get_calculation_age_groups(self, age, panel):
        if panel in [0, 5]:
            panel_to_mid_age_group = 10
        elif panel in [70, 75]:
            panel_to_mid_age_group = 70
        else:
            panel_to_mid_age_group = 5 * floor(age / 5)
        #print(panel_to_mid_age_group)
        age_groups = []
        offset = -10
        for i in range(5):
            age_groups.append(panel_to_mid_age_group + offset)
            offset = offset + 5
        populations = []
        return age_groups


    def set_by_age_groups(self, age_groups, reset=True, max_age=79):
        if reset:
            self.ages = {}
        for age in range(0, max_age+1):
            #print(age)
            panel_key, n = self._get_multipliers_panel_and_n(age)
            #print(panel_key, n)
            multiplier = _multipliers[panel_key][n]
            #print(multiplier)
            calc_age_groups = self._get_calculation_age_groups(age, panel_key)
            #print(calc_age_groups)
            population_groups = []
            for group in calc_age_groups:
                population_groups.append(age_groups[group][2])
            #print(population_groups)
            total_age = 0
            for i in range(5):
                total_age += population_groups[i] * multiplier[i]
            self.ages[age] = total_age
            #print()


    def get_population_for_ages(self, entry_age, duration):
        result = 0
        for age in range(entry_age, entry_age + duration):
            #print(age)
            if age in self.ages:
                result += self.ages[age]
            else:
                pass #TODO raise Exception?
        return result
