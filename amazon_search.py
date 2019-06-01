# coding: shift-jis
from bs4 import BeautifulSoup
import requests
import pandas as pd
import csv

__author__ = "SakaiEiji"
__version__ = "1.0.0"
__date__    = "2019/05/25"

# �A�}�]���Ō������������t�������� �������ʂ́u���i���v�Ɓu�l�i�v��CSV�ɕۑ�����
def search_amazon(search_word):
    """
    ���͂��ꂽ�L�[���[�h�̌������ʃy�[�W����HTML����͂���
    ���i���A�l�i��CSV�o�͂���
    �Ȃ��A��������y�[�W�̓T�C�g�̕��ׂ𓥂܂��u5�y�[�W�v�܂łƂ���

    @param search_word : this is a first param
    @raise keyError: raises an exception
    """

    # �A�}�]���̃x�[�X�ƂȂ�URL
    amazon = "https://www.amazon.co.jp"

    # �󔒂ŕ���
    words = search_word.split(" ")
    # �擪�L�[���[�h�擾
    serch_words = words[0]
    # ������2�ڈȍ~�̃L�[���[�h��+�ŘA��
    for i in range(1, len(words)):
        serch_words = serch_words + "+" + words[i]

    # �X�N���C�s���O����T�C�g��URL���쐬
    url =  amazon + "/s/ref=nb_sb_noss_2?__mk_ja_JP=�J�^�J�i&url=search-alias%3Daps&field-keywords=" + serch_words + "&rh=i%3Aaps%2Ck%3A" + serch_words

    # CSV�̃w�b�_�[�ɏ����݂��鍀�ڂ����X�g�ō쐬
    columns = ["Name",  "Price"]
    # �z�񖼂��w�肷��
    df = pd.DataFrame(columns=columns)

    # �y�[�W�ԍ�(1�y�[�W�ڂ���)
    page = 1

    #�@6�y�[�W�����́uexcept�v������
    try:

        #�@�T�C�g�̕��ׂ��l�����A1?5�y�[�W�������J��Ԃ�
        while page < 6:

            # �쐬����URL����HTML���擾
            response = requests.get(url).text
            # BeautifulSoup�̏�����
            soup = BeautifulSoup(response, 'html.parser')

            # html�̂ǂ̕������擾���邩�w��
            items = soup.find_all(attrs={'class':'s-result-item'})

            # �擾�����^�O�S��1������
            for item in items:

                # ���i���̃^�O�擾
                name = item.find("span", {"class":"a-size-base-plus a-color-base a-text-normal"})
                # �l�i�̃^�O�擾
                price = item.find("span", {"class":"a-offscreen"})

                # ���i���A�l�i�̕Е������Ȃ��ꍇ��CSV�o�͂����A���̃��[�v��(�G���[�ƂȂ邽��)
                if name == None or price == None:
                    continue

                # ���i���擾
                nameTitle = name.string
                # ���i�̒l�i�擾
                priceText = price.string

                # ���i���A�l�i�����X�g�ɒǉ�
                se = pd.Series([nameTitle, priceText], columns)
                #���X�g��ǉ�
                df = df.append(se, columns)

            # �u���̃y�[�W�v�{�^���̃^�O���擾
            nextButton = soup.find("li", {"class":"a-last"})

            # �u���̃y�[�W�v�{�^����URL���擾
            nextUrl = nextButton.a.get("href")

            # �A�}�]���̃x�[�X�ƂȂ�URL + ���y�[�W��URL
            url = amazon + nextUrl
            # ���̃y�[�W�ɍs���̂�+1����
            page += 1

    except:

             # �������ʂ�2�y�[�W���A5�y�[�W�܂łȂ��ꍇ�͈ȉ����o��
             print(page +1 + "�ȍ~�̃y�[�W�͂���܂���ł���")

    finally:

        # �ۑ�����csv�̃t�@�C���������߂�
        filename = "amazon_" + search_word + ".csv"
        # �쐬�������X�g��csv��
        df.to_csv(filename, encoding = 'utf-8-sig')
        # �I�������|���o��
        print("�I�����܂���")



# �����L�[���[�h����͂���
print('Amazon�̏��i���������܂�\n�������[�h����͂��Ă�������')
key_word = input('�������[�h:')

# �����L�[���[�h�Ō��������{(serch_amazon���\�b�h�ďo)
search_amazon(key_word)