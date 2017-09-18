def cal(l, m):
    # 字母位置l，最大移动步m，返回最多连续
    # 最笨的算法：枚举(应该有更好的加速算法)
    length = len(l)
    maxN = 0
    for i in range(length):
        jz = i - 1  # 左侧
        jy = i + 1  # 右侧
        n = 1  # 最大连续个数
        d = 0  # 总距离
        dz = None  # 左边距离（用于加速运算）
        dy = None  # 右边距离（用于加速运算）
        cd = 0  # 当次取的距离（用于加速运算）
        while jz > -1 or jy < length:
            if dz is None and jz > -1:
                dz = l[i] - l[jz] - (i - jz)  # 左边距离
            if dy is None and jy < length:
                dy = l[jy] - l[i] - (jy - i)  # 右边距离
            if dz is None and dy is None:  # 两边都没有了
                break
            elif dz is None:  # 没有左边了
                cd = dy
                dy = None  # 取哪边下次计算哪边
                jy += 1
            elif dy is None:  # 没有右边了
                cd = dz
                dz = None
                jz -= 1
            elif dz <= dy:  # 取距离小的
                cd = dz
                dz = None
                jz -= 1
            else:
                cd = dy
                dy = None
                jy += 1
            if d + cd > m:		# 大于最大次数了
                break
            elif m - d - cd < cd - 1:  # 下次肯定大于了（加速）
                n += 1
                break
            else:  # 接着算吧
                n += 1
                d += cd
        if n > maxN:  # 出循环了，计算最大的n存下来
            maxN = n
    return maxN


def find(S, m):
    d = {}
    for i in range(97, 123):
        d[chr(i)] = []  # 26个字母位置数组
    i = 0
    for s in S:
        d[s].append(i)
        i += 1
    l = sorted(d.items(), key=lambda x: len(x[1]), reverse=True)  # 按照字母数量排序
    maxN = 0
    for i in l:
        if len(i[1]) <= maxN:  # 数量都不大于最大值就别算了（加速）
            break
        n = cal(i[1], m)  # i[1]字母位置数组, 返回结果
        if n > maxN:
            maxN = n  # 如果要记录最大的字母把i[0]记录下来就行了
    return maxN


if __name__ == '__main__':
    # S = 'abcdzbaxvna'
    # m = 3
    """a = input()
    b = a.split(' ')
    S = b[0]
    m = int(b[1])"""
    S = 'ecbxooxtqjrlvnorhxeglkoxwfdvswfeeoctyjiqsfkgylwgqjrvrubkjxpbsygglxpelreeztwnlzrfcrtvrqnoveuoqsqfneyphortytzcdswuvwvmootjbzxuctgcvmjkfqtbnklxhtiyoclcosthhxntrzwshgnyntqvvourhsdbgqcwrnkbymqcofypmzumkqzrnsylgfwqmprbfjxnhiowvjdnjgifujnxquxuiswkjkrqbhoyfwyghrddqrhbbdcbcuxcbnlhemgbkpokshcouzsxhwzokvjblwepdoqvvpqztmghrmrsfissbnqyndzqrjdxjgqhhwkjujursybqkqcdtfwznenytqcdrvyqdoddbobrwrblejpkwzupkksdnlxfjivmxlpeccybngxzrmrfesqgwnqlkmoyryyvdpcovzbwhkzllfjvmldxvhmrekduwnldgltehhsycfljgebgsxljywtnofdjmkkdcxtrtzlzmbnfrtzwcipffopdshkdwdylhsvwyybvlpwvgdedzlsvqkirmvoukvptxmxutmvwtzrnwdwvpklcihbdxchtspgsrkyyrrgugnfgbutdoxewrnlwkxjomiotscebubsrufrksmsjcqulpmqqdyqovwwduppyiptjbygkbbpksfbjntylfwbwxgmcesdstrylkfnngkixfwfiulvsbbltdvqhsurxsmqydixcsikjwzdjjibnbreecrfhpezkesrjwzendqfglnjemivktrmylpuosuheembjvkqdhqjzrwwkvekiwkmgzctddwomdtcbvthjjsmtbkvuvxxnhljecsndygolyqtidmkqhcwtjhtydtlnmtmytcvqjfovbdscgyycwjqtfwinsrcqxmcwdhtnkhbgtgtcgrsvxywjifopnviymddnvtlpriirdihntqnpdogusxdcmlgsrnfxnqlysqpheblwvwtufsbsmtrhxovb'
    m = 6
    print(find(S, m))
