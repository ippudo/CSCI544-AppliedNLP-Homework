<?PHP
require_once("p_regex.php");
$debug=0;
#$rea_jp_title $rea_review

function getJson($url)
{
   $result=json_decode(file_get_contents($url));
   return $result;
}

function postdata($data,$url)
{
    global $debug;
    $post_data=('episode_id='.$eid);
    $posturl='http://bangumi.bilibili.com/web_api/get_source';
    $postepisode=curl_init();
    curl_setopt($postepisode,CURLOPT_POST,1);
    curl_setopt($postepisode,CURLOPT_HEADER,0);
    curl_setopt($postepisode,CURLOPT_URL,$posturl);
    curl_setopt($postepisode,CURLOPT_POSTFIELDS,$post_data);
    curl_setopt($postepisode, CURLOPT_RETURNTRANSFER, 1);
    return curl_exec($postepisode);
}

#Return string based json
function getJPProductidByRankingid($rid)
{
    global $rea_jp_title;
    $geturl="https://www.amazon.co.jp/gp/bestsellers/books/".$rid."/?ie=UTF8&pg=";
    $pid=array();
    for ($i=1;$i<=5;$i++)
    {
        $data=file_get_contents($geturl.$i);
        $matches=array();
        preg_match_all($rea_jp_title,$data,$matches,PREG_SET_ORDER);
        if (count($matches)<1)
        {
            $i--;
            print ("retry ".$i."\n");
            sleep(1);
            continue;
        }

        foreach ($matches as $match)
        {
            array_push($pid,$match[1]);
        }
        print ("get ".count($matches)." at ".$i."\n");
        sleep(2);
    }
    return $pid;
}

function getJPReviewsByProductid($pid,$style)
{
    global $rea_review,$rea_jp_totalreview,$rrr_br;
    $geturl="https://www.amazon.co.jp/product-reviews/".$pid."/?ie=UTF8&filterByStar=".$style."&pageNumber=";
    $data="";
    $rcount=array();
    $review=array();
    $match_result=0;
    for ($ifo=0;$ifo<5&&$match_result==0;$ifo++)
    {
        $match_result=preg_match($rea_jp_totalreview,$data,$rcount);
        $data=file_get_contents($geturl);
    }
    $reviewcount=$match_result?$rcount[1]:0;
    print ("Total reviews:".$reviewcount."\n");
    for ($i=1;$i<=ceil($reviewcount/10);$i++)
    {
        $data=file_get_contents($geturl.$i);
        $matches=array();
        preg_match_all($rea_review,$data,$matches,PREG_SET_ORDER);
        if (count($matches)<1)
        {
            $i--;
            print ("retry ".$i."\n");
            sleep(1);
            continue;
        }
        foreach ($matches as $match)
        {
            array_push($review,preg_replace($rrr_br,"\n",$match[1]));
        }
        print ("get ".count($matches)." at ".$i."\n");
        sleep(1);
    }
    return $review;
}

function grab()
{
$rankinglist=[503566,492380,492372,746112,492374,492386,531712];
foreach($rankinglist as $ranking)
{
    print("RankList ".$ranking."\n");
    $booklist=getJPProductidByRankingid($ranking);

    foreach($booklist as $book)
    {
        print ("Now Dealing with ".$book."\n");
        $rcount=0;
        $creview=getJPReviewsByProductid($book,"critical");
        foreach($creview as $r)
        {
            $rcount++;
            file_put_contents("critical/".$book."-".$rcount.".txt",$r);
        }
        $rcount=0;
        $greview=getJPReviewsByProductid($book,"positive");
        foreach($greview as $r)
        {
            $rcount++;
            file_put_contents("positive/".$book."-".$rcount.".txt",$r);
        }

    }
}
}

grab();

#$a=getJPReviewsByProductid(4592761790,"positive");


#$j=getJson("http://product.dangdang.com/comment/comment.php?product_id=23974513&datatype=1&page=1&filtertype=1&sysfilter=1");
#$var=getBangumiByPID("123");
#var_dump($var);
#$isbns=getDangdangPIDByISBN("9787505135949");
#var_dump($isbns);
#var_dump(getDataByISBN("9787505135949"));
#var_dump(getDataByISBN("978-4062836029"));
#getDataByISBN("978-4062836029");
?>
