'''配置文件'''


ROOT_DIR = 'resources'
ACTION_DISTRIBUTION = [['1', '11', '15', '26'],
					   ['5', '6', '7', '8', '9', '10'],
					   ['16', '17'],
					   ['18', '20', '21'],
					   ['22'],
					   ['30', '31', '32', '33'],
					   ['34', '35', '36', '37']]
PET_ACTIONS_MAP = {'pet_39': ACTION_DISTRIBUTION}
# for i in range(2, 65): PET_ACTIONS_MAP.update({'pet_%s' % i: ACTION_DISTRIBUTION})