#include <iostream>
#include <vector>
#include <map>
using namespace std;


int cal(vector<int> l, int m){
	//字母位置l，最大移动步m，返回最多连续
    //最笨的算法：枚举(应该有更好的加速算法)
    int length = l.size();
    int maxN = 0;
    for(int i=0;i<length;i++){
    	int jz = i - 1;  // 左侧
        int jy = i + 1;  // 右侧
        int n = 1;  // 最大连续个数
        int d = 0;  // 总距离
        int dz = -1;  // 左边距离（用于加速运算）
        int dy = -1;  // 右边距离（用于加速运算）
        int cd = 0;  // 当次取的距离（用于加速运算）
        while(jz > -1 || jy < length){
        	if(dz < 0 && jz > -1)
                dz = l[i] - l[jz] - (i - jz);  // 左边距离
            if(dy < 0 && jy < length)
                dy = l[jy] - l[i] - (jy - i);  // 右边距离
            if(dz < 0 and dy < 0)  // 两边都没有了
                break;
            else if(dz < 0){  // 没有左边了
                cd = dy;
                dy = -1;  // 取哪边下次计算哪边
                jy += 1;
            }
            else if(dy < 0){  // 没有右边了
                cd = dz;
                dz = -1;
                jz -= 1;
            }
            else if(dz <= dy){  // 取距离小的
                cd = dz;
                dz = -1;
                jz -= 1;
            }
            else{
                cd = dy;
                dy = -1;
                jy += 1;
            }
            if(d + cd > m)		// 大于最大次数了
                break;
            else if(m - d - cd < cd - 1){  // 下次肯定大于了（加速）
                n += 1;
                break;
            }
            else{  // 接着算吧
                n += 1;
                d += cd;
            }
        }
        if(n > maxN)  // 出循环了，计算最大的n存下来
            maxN = n;
    }
    return maxN;
}


bool cmp(const pair<char, vector<int> >& x, 
   		 const pair<char, vector<int> >& y){
	return x.second.size() > y.second.size();
}


int find(string S, int m){
    map<char, vector<int> > d;
    //for(int i=97;i<123;i++)
    //    d[char(i)] = new vector<int>();  // 26个字母位置数组
    int length = S.length();
    for(int i=0;i<length;i++)
        d[S[i]].push_back(i);
    vector<pair<char, vector<int> > > p(d.begin(), d.end());
   	sort(p.begin(), p.end(), cmp);
   	int maxN = 0;
   	int n = 0;
   	vector<pair<char, vector<int> > >::iterator it;
   	it = p.begin();
    while(it != p.end()){
        if(int(it->second.size()) <= maxN)  // 数量都不大于最大值就别算了（加速）
            break;
        n = cal(it->second, m);
        if(n > maxN)
            maxN = n;  // 如果要记录最大的字母把it->first记录下来就行了
        it++;
    }
    return maxN;
}

int main(){
    string S = "ecbxooxtqjrlvnorhxeglkoxwfdvswfeeoctyjiqsfkgylwgqjrvrubkjxpbsygglxpelreeztwnlzrfcrtvrqnoveuoqsqfneyphortytzcdswuvwvmootjbzxuctgcvmjkfqtbnklxhtiyoclcosthhxntrzwshgnyntqvvourhsdbgqcwrnkbymqcofypmzumkqzrnsylgfwqmprbfjxnhiowvjdnjgifujnxquxuiswkjkrqbhoyfwyghrddqrhbbdcbcuxcbnlhemgbkpokshcouzsxhwzokvjblwepdoqvvpqztmghrmrsfissbnqyndzqrjdxjgqhhwkjujursybqkqcdtfwznenytqcdrvyqdoddbobrwrblejpkwzupkksdnlxfjivmxlpeccybngxzrmrfesqgwnqlkmoyryyvdpcovzbwhkzllfjvmldxvhmrekduwnldgltehhsycfljgebgsxljywtnofdjmkkdcxtrtzlzmbnfrtzwcipffopdshkdwdylhsvwyybvlpwvgdedzlsvqkirmvoukvptxmxutmvwtzrnwdwvpklcihbdxchtspgsrkyyrrgugnfgbutdoxewrnlwkxjomiotscebubsrufrksmsjcqulpmqqdyqovwwduppyiptjbygkbbpksfbjntylfwbwxgmcesdstrylkfnngkixfwfiulvsbbltdvqhsurxsmqydixcsikjwzdjjibnbreecrfhpezkesrjwzendqfglnjemivktrmylpuosuheembjvkqdhqjzrwwkvekiwkmgzctddwomdtcbvthjjsmtbkvuvxxnhljecsndygolyqtidmkqhcwtjhtydtlnmtmytcvqjfovbdscgyycwjqtfwinsrcqxmcwdhtnkhbgtgtcgrsvxywjifopnviymddnvtlpriirdihntqnpdogusxdcmlgsrnfxnqlysqpheblwvwtufsbsmtrhxovb";
    int m = 200;
    cout<<find(S, m)<<endl;
    return 0;
}