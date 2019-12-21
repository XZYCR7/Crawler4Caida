﻿# coding:utf-8"""create on Dec 18, 2019 by Wayne YUFunction:处理as_core_map的数据，生成极坐标，并绘图对绘图进行优化"""import timeimport csvimport numpy as npimport matplotlib.pyplot as pltdef write_to_csv(res_list, des_path):    """    把给定的List，写到指定路径的文件中    :param res_list:    :param des_path:    :return: None    """    print("write file <%s> ..." % des_path)    csvFile = open(des_path, 'w', newline='', encoding='utf-8')    try:        writer = csv.writer(csvFile, delimiter="|")        for i in res_list:            writer.writerow(i)    except Exception as e:        print(e)    finally:        csvFile.close()    print("write finish!")def compute_polar_args(as_info):    """    根据传入的as_info,计算每个as号的参数angle、radius    angle = longitue of the AS's orgs    radius = 1 - log((All_rel(AS)+1) / (maxinum_all_rel + 1))    :param as_info:    :return new_as_info:    """    new_as_info = []    max_all_rel = 0  # 存储最大的连接数    for item in as_info:        # print(item)        if int(item[1]) > max_all_rel:            max_all_rel = int(item[1])    print("Max Edge Cnt:", max_all_rel)    for item in as_info:        angle = 0.0        radius = 0.0        if float(item[10]) >= 0.0:            angle = float(item[10])        else:            angle = float(item[10]) + 360.0        radius = 1 - np.log((int(item[1]) + 1) / (max_all_rel + 1))        item.append(angle)        item.append(radius)        new_as_info.append(item)        # print(item)    return new_as_infodef draw_polar_map(as_info, open_file, year_str):    """    根据传入的as_info进行绘图    :param as_info:    :param open_file:    :param year_str:    :return None:    """    # #########################关键参数生成##################################    max_radius = 0.0    min_radius = 10000.0    min_index = 0    angle_list = []    radius_list = []    coordinate_dic = {}    temp_list = []    item_cnt = 0    for item in as_info:        print(item)        if float(item[12]) > max_radius:            max_radius = float(item[12])        if float(item[12]) < min_radius:            min_radius = float(item[12])            min_index = item_cnt        angle = (float(item[11]) / 360.0) * 2 * np.pi        radius = float(float(item[12]))        temp_list.append(angle)        temp_list.append(radius)        angle_list.append(angle)        radius_list.append(radius)        coordinate_dic[item[0]] = temp_list        temp_list = []        item_cnt += 1    # print(coordinate_dic)    # 准备绘图    # colors = angle_list    ax = plt.subplot(111, projection='polar')    ax.set_ylim(0.0, max_radius + 2)  # 设置极坐标半径radius的最大刻度    # #########################绘画参数生成##################################    area_list = []    lw_list = []    c_color_list = []    z_order_list = []    max_index = []    cn_index = []    index_cnt = 0    for item in radius_list:        if item < max_radius * 0.2:            area_list.append(12)            lw_list.append(0.8)            c_color_list.append([1, 0, 0])            z_order_list.append(2)            max_index.append(index_cnt)  # 记录最牛逼的几个点的坐标            if as_info[index_cnt][8] == "CN":                cn_index.append(index_cnt)        elif item < max_radius * 0.4:            area_list.append(8)            lw_list.append(0.4)            c_color_list.append([0, 1, 0])            z_order_list.append(2)            if as_info[index_cnt][8] == "CN":                cn_index.append(index_cnt)        elif item < max_radius * 0.6:            area_list.append(3)            lw_list.append(0.2)            c_color_list.append([0, 0, 1])            z_order_list.append(2)            if as_info[index_cnt][8] == "CN":                cn_index.append(index_cnt)        else:            area_list.append(1)            lw_list.append(0.1)            c_color_list.append([1, 1, 1])            z_order_list.append(1)        index_cnt += 1    area = area_list    # ###########################画线################################    file_read = open(open_file, 'r', encoding='utf-8')    for line in file_read.readlines():        if line.strip().find("#") == 0:            continue        line = line.strip().split("|")        p1 = coordinate_dic.get(line[0])        p2 = coordinate_dic.get(line[1])        if p1 and p2:            z_order_value = 1            line_width = 0.05            alpha_value = 1            if p1[1] < max_radius * 0.2 and p2[1] < max_radius * 0.2:                line_width = 0.4                line_color = [0.9, 0.2, 0.2]                alpha_value = 1                z_order_value = 4            elif p1[1] < max_radius * 0.4 and p2[1] < max_radius * 0.4:                line_width = 0.2                line_color = [0.4, 0.4, 0.9]                alpha_value = 0.7                z_order_value = 3            elif p1[1] < max_radius * 0.6 and p2[1] < max_radius * 0.6:                line_width = 0.1                line_color = [0.5, 0.5, 0.9]                alpha_value = 0.5                z_order_value = 2            else:                line_width = 0.02                line_color = [0, 1, 1]                z_order_value = 1            print("computing:", p1, p2)            ax.plot([p1[0], p2[0]], [p1[1], p2[1]], linewidth=line_width, alpha=alpha_value, color=line_color, zorder=z_order_value, )    # ######################## 打点######################################    c = ax.scatter(angle_list, radius_list, c=c_color_list, edgecolors=[0, 0, 0], marker='s', lw=lw_list, s=area, cmap='hsv', alpha=0.8, zorder=5)    # c = ax.scatter(angle_list, radius_list, c=colors, marker='s', s=area, cmap='hsv', alpha=1)    # ########################绘制外围辅助性图标##########################    # 画个内圆    circle_theta = np.arange(0, 2*np.pi, 0.01)    circle_radius = [max_radius + 0.1] * len(circle_theta)    # print(circle_theta)    # print(circle_radius)    ax.plot(circle_theta, circle_radius, color=[0, 0, 0], linewidth=0.2)    # 画个外圆1    circle_theta = np.arange(0, 2*np.pi, 0.01)    circle_radius = [max_radius + 0.3] * len(circle_theta)    # print(circle_theta)    # print(circle_radius)    ax.plot(circle_theta, circle_radius, color=[0, 0, 0], linewidth=0.2)    # 画外圆2    circle_theta = np.arange(0, 2*np.pi, 0.01)    circle_radius = [max_radius + 0.5] * len(circle_theta)    # print(circle_theta)    # print(circle_radius)    ax.plot(circle_theta, circle_radius, color=[0, 0, 0], linewidth=0.2)    # 画外圆3    circle_theta = np.arange(0, 2*np.pi, 0.01)    circle_radius = [max_radius + 0.6] * len(circle_theta)    # print(circle_theta)    # print(circle_radius)    ax.plot(circle_theta, circle_radius, color=[0, 0, 0], linewidth=0.2)    # 填充欧洲（Europe）颜色为#bd87bf，从西经14度至东经49度，即346-49    circle_theta = np.arange(float(346.0/360)*2*np.pi, float(360/360)*2*np.pi, 0.01)    circle_radius = [max_radius + 0.2] * len(circle_theta)    ax.plot(circle_theta, circle_radius, color="#bd87bf", linewidth=3)    circle_theta = np.arange(float(0.0/360)*2*np.pi, float(49/360)*2*np.pi, 0.01)    circle_radius = [max_radius + 0.2] * len(circle_theta)    ax.plot(circle_theta, circle_radius, color="#bd87bf", linewidth=3)    # 填充亚洲（Asia）颜色为#00a895,从东经49度至西经175，即49-185    circle_theta = np.arange(float(49.0/360)*2*np.pi, float(185/360)*2*np.pi, 0.01)    circle_radius = [max_radius + 0.2] * len(circle_theta)    ax.plot(circle_theta, circle_radius, color="#00a895", linewidth=3)    # 填充北美洲（North American）颜色为#669ed8，从西经170度至西经20度，即190-340    circle_theta = np.arange(float(190.0/360) * 2 * np.pi, float(340/360) * 2 * np.pi, 0.01)    circle_radius = [max_radius + 0.2] * len(circle_theta)    ax.plot(circle_theta, circle_radius, color="#669ed8", linewidth=3)    # 填充非洲（Africa）颜色为#b680c3，从西经14度至东经52度，即346-52    circle_theta = np.arange(float(346.0/360) * 2 * np.pi, float(360/360) * 2 * np.pi, 0.01)    circle_radius = [max_radius + 0.4] * len(circle_theta)    ax.plot(circle_theta, circle_radius, color="#f3c828", linewidth=3)    circle_theta = np.arange(float(0.0/360) * 2 * np.pi, float(52/360) * 2 * np.pi, 0.01)    circle_radius = [max_radius + 0.4] * len(circle_theta)    ax.plot(circle_theta, circle_radius, color="#f3c828", linewidth=3)    # 填充大洋洲(Oceana)，颜色为#fec273，从东经110度至东经180度，即110-180    circle_theta = np.arange(float(110/360) * 2 * np.pi, float(180/360) * 2 * np.pi, 0.01)    circle_radius = [max_radius + 0.4] * len(circle_theta)    ax.plot(circle_theta, circle_radius, color="#fec273", linewidth=3)    # 填充南美洲（South American），颜色为#f2c41d，从西经80度至西经40度，即280-320    circle_theta = np.arange(float(280/360) * 2 * np.pi, float(320/360) * 2 * np.pi, 0.01)    circle_radius = [max_radius + 0.4] * len(circle_theta)    ax.plot(circle_theta, circle_radius, color="#f2c41d", linewidth=3)    # 绘制经度刻度    # circle_radius = np.arange(max_radius+0.5, max_radius+0.9, 0.01)    # circle_theta = [0.0] * len(circle_radius)    # ax.plot(circle_theta, circle_radius, color=[0, 0, 0], linewidth=0.8)    # 每隔10度画一个    for tap_zone in range(0, 36, 1):        time_zone_angle = tap_zone * 10        circle_radius = np.arange(max_radius + 0.55, max_radius + 0.8, 0.01)        circle_theta = [float(time_zone_angle / 360)*2*np.pi] * len(circle_radius)        ax.plot(circle_theta, circle_radius, color=[0, 0, 0], linewidth=0.3)    # 每隔90度画一个    for tap_zone in range(0, 4, 1):        time_zone_angle = tap_zone * 90        circle_radius = np.arange(max_radius + 0.55, max_radius + 0.9, 0.01)        circle_theta = [float(time_zone_angle / 360)*2*np.pi] * len(circle_radius)        ax.plot(circle_theta, circle_radius, color=[0, 0, 0], linewidth=1)    # 添加关键城市和地区的文本信息    # 一般字体统一用一个字典控制    font = {'family': 'serif',            'style': 'italic',            'weight': 'normal',            'color': 'black',            'size': 4            }    text_theta = 0.0    text_radius = max_radius + 1    ax.text(text_theta, text_radius, "London, UK", fontdict=font,  ha='left', va='center', rotation=0)    text_theta = float(5.0/360)*2*np.pi    text_radius = max_radius + 1    ax.text(text_theta, text_radius, "Paris, FR", fontdict=font, ha='left',  va='bottom', rotation=5)    text_theta = float(9.0/360)*2*np.pi    text_radius = max_radius + 1    ax.text(text_theta, text_radius, "Frankfurt, DE", fontdict=font, ha='left',  va='bottom', rotation=9)    text_theta = float(15.0/360)*2*np.pi    text_radius = max_radius + 1    ax.text(text_theta, text_radius, "Berlin, DE", fontdict=font, ha='left',  va='bottom', rotation=15)    text_theta = float(27.0/360)*2*np.pi    text_radius = max_radius + 1    ax.text(text_theta, text_radius, "Helsinki, FI", fontdict=font, ha='left',  va='bottom', rotation=27)    text_theta = float(39.0/360)*2*np.pi    text_radius = max_radius + 1    ax.text(text_theta, text_radius, "Moscow, RU", fontdict=font, ha='left',  va='bottom', rotation=39)    text_theta = float(75.0/360)*2*np.pi    text_radius = max_radius + 1    ax.text(text_theta, text_radius, "Bombay, IN", fontdict=font, ha='left',  va='bottom', rotation=75)    text_theta = float(78.0/360)*2*np.pi    text_radius = max_radius + 1    ax.text(text_theta, text_radius, "Delhi, IN", fontdict=font, ha='left',  va='bottom', rotation=78)    text_theta = float(100.0/360)*2*np.pi    text_radius = max_radius + 1    ax.text(text_theta, text_radius, "Bangkok, TH", fontdict=font, ha='right',  va='bottom', rotation=100)    text_theta = float(102.0/360)*2*np.pi    text_radius = max_radius + 1    ax.text(text_theta, text_radius, "Singapore, SG", fontdict=font, ha='right',  va='bottom', rotation=102)    text_theta = float(116.0/360)*2*np.pi    text_radius = max_radius + 1    ax.text(text_theta, text_radius, "Beijing, CN", fontdict=font, ha='right',  va='bottom', rotation=116)    text_theta = float(121.0/360)*2*np.pi    text_radius = max_radius + 1    ax.text(text_theta, text_radius, "Taiopei, CN", fontdict=font, ha='right',  va='bottom', rotation=121)    text_theta = float(139.0/360)*2*np.pi    text_radius = max_radius + 1    ax.text(text_theta, text_radius, "Tokyo, JP", fontdict=font, ha='right',  va='bottom', rotation=139)    text_theta = float(151.0/360)*2*np.pi    text_radius = max_radius + 1    ax.text(text_theta, text_radius, "Sydney, AU", fontdict=font, ha='right',  va='bottom', rotation=151)    text_theta = float(201/360)*2*np.pi    text_radius = max_radius + 1    ax.text(text_theta, text_radius, "Honolulu, US", fontdict=font, ha='right',  va='top', rotation=201)    text_theta = float(238.0/360)*2*np.pi    text_radius = max_radius + 1    ax.text(text_theta, text_radius, "San Jose, US", fontdict=font, ha='right',  va='top', rotation=238)    text_theta = float(242.0/360)*2*np.pi    text_radius = max_radius + 1    ax.text(text_theta, text_radius, "San Diego, US", fontdict=font,  ha='right',  va='top', rotation=242)    text_theta = float(248.0/360)*2*np.pi    text_radius = max_radius + 1    ax.text(text_theta, text_radius, "Phoenix, US", fontdict=font,  ha='right',  va='top', rotation=248)    text_theta = float(255.0/360) * 2 * np.pi    text_radius = max_radius + 1    ax.text(text_theta, text_radius, "Denver, US", fontdict=font,  ha='right',  va='top', rotation=255)    text_theta = float(263.0/ 360) * 2 * np.pi    text_radius = max_radius + 1    ax.text(text_theta, text_radius, "Houston, US", fontdict=font,  ha='right',  va='top', rotation=263)    text_theta = float(272.0/360) * 2 * np.pi    text_radius = max_radius + 1    ax.text(text_theta, text_radius, "Chicago, US", fontdict=font,  ha='center',  va='top', rotation=272)    text_theta = float(281.0/ 360) * 2 * np.pi    text_radius = max_radius + 1    ax.text(text_theta, text_radius, "Toronto, CA", fontdict=font,  ha='left',  va='top', rotation=281)    text_theta = float(284.0/360) * 2 * np.pi    text_radius = max_radius + 1    ax.text(text_theta, text_radius, "Washington, US", fontdict=font, ha='left',  va='top', rotation=284)    text_theta = float(286.0/360) * 2 * np.pi    text_radius = max_radius + 1    ax.text(text_theta, text_radius, "Ottawa, CA", fontdict=font, ha='left',  va='top', rotation=286)    text_theta = float(289.0/360) * 2 * np.pi    text_radius = max_radius + 1    ax.text(text_theta, text_radius, "Boston, US", fontdict=font, ha='left',  va='top', rotation=289)    text_theta = float(302.0/360) * 2 * np.pi    text_radius = max_radius + 1    ax.text(text_theta, text_radius, "Buenos Aires, AR", fontdict=font, ha='left',  va='top', rotation=302)    text_theta = float(316.0/360) * 2 * np.pi    text_radius = max_radius + 1    ax.text(text_theta, text_radius, "Rio de Janeiro, BR", fontdict=font, ha='left',  va='top', rotation=316)    text_theta = float(351.0/360) * 2 * np.pi    text_radius = max_radius + 1    ax.text(text_theta, text_radius, "ALges, PT", fontdict=font, ha='left',  va='top', rotation=351)    text_theta = float(354.0/360) * 2 * np.pi    text_radius = max_radius + 1    ax.text(text_theta, text_radius, "Dublin, IE", fontdict=font, ha='left',  va='top', rotation=354)    # 给最牛逼的几个点做标记    # 一般字体统一用一个字典控制    font = {'family': 'serif',            'style': 'italic',            'weight': 'normal',            'color': 'black',            'size': 2            }    for index_item in max_index:        as_string = as_info[index_item][5] + "(AS"+as_info[index_item][0]+")"        # as_string ="AS" + as_info[index_item][0]        ax.text(angle_list[index_item]-0.2, radius_list[index_item]+0.1, as_string, fontdict=font, ha='right', va='center', zorder=6)    # 给中国几个牛逼的AS做标记    font = {'family': 'serif',            'style': 'italic',            'weight': 'normal',            'color': 'black',            'size': 2            }    for index_item in cn_index:        as_string = "AS"+as_info[index_item][0]        ax.text(angle_list[index_item], radius_list[index_item]+0.1, as_string, fontdict=font, ha='right', va='center', zorder=6)    print(as_info[0])  # 测试    print("连通度最高的AS号半径：", radius_list[min_index], "ASN:", as_info[min_index][0], "AS info:", as_info[min_index][5])    # 画出圆心    # ax.scatter(0, 0, c="", edgecolors=[0, 0, 0], marker='o', lw=1, s=0.5, cmap='hsv', alpha=0.8, zorder=5)    plt.axis('off')    # plt.xticks([])  # 去掉横坐标    # plt.yticks([])  # 去掉纵坐标    save_fig_name = "../000LocalData/as_image/as_core_map" + year_str + ".jpg"    plt.savefig(save_fig_name, dpi=1080)    # plt.show()    plt.close()if __name__ == "__main__":    time_start = time.time()  # 记录启动时间    # year_string = "2009"    for year_string in range(2010, 2020, 1):        file_in = '..\\000LocalData\\as_map\\as_core_map_data_new' + str(year_string) + '1001.csv'        file_read = open(file_in, 'r', encoding='utf-8')        file_in_list = []        new_info = []        asn_temp = ""        for line in file_read.readlines():            line = line.strip().split('|')            if len(line) < 11:                continue            if asn_temp == line[0]:                continue            file_in_list.append(line)            asn_temp = line[0]        new_info = compute_polar_args(file_in_list)  # 计算极坐标相关参数        bgp_file = "..\\000LocalData\\as_relationships\\serial-1\\" + str(year_string) + "1001.as-rel.txt"        draw_polar_map(new_info, bgp_file, str(year_string))    # print(file_in_list)    time_end = time.time()    print("=>Scripts Finish, Time Consuming:", (time_end - time_start), "S")