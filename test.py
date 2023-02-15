import json
import logging    
import os

logger = logging.getLogger(__name__)
logger.setLevel(level = logging.INFO)

def _get_config():
    """get json"""
    config_path = os.getcwd() + os.sep + 'TaobaoAutoBuy' + os.sep +'config.json'
    print(config_path)
    try:
        with open(config_path) as f:
            config = json.loads(f.read())
            return config
    except ValueError:
        logger.error(u'config.json Format Error')
        sys.exit()

def _analyze_xpath(config):
    shopID = config['shopID']
    click_list = []
    for shopid in shopID:
        str_item = '//*[@id="J_Order_s_'+ shopid + '_1"]/div[1]/div/div'
        click_list += [str_item]
    print(click_list)
    return click_list




    



if __name__ == '__main__':
    try:
        config = _get_config()
        _analyze_xpath(config)
        logger.info('Finished\n')
        '''
        print(config['clock'])
        print(config['shopID'])
        print(type(config['shopID']))
        print(config['shopITEM'])
        print(type(config['shopITEM']))
        shopitem = config['shopITEM']
        print(shopitem[0])
        print(shopitem[1])
        print(shopitem[-1])
        print(len(shopitem))
        print(len(config['shopID']))
        '''



    except Exception as e:
        logger.exception(e)
        logger.info('\n')