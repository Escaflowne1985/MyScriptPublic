<p>基于百度AI图文创作功能启发，由于限制ixu是是百家号的文章，其他比如说头条、企鹅号、搜狐号、网易号、大风号、大鱼号这里面的文章就好使了。想要做这些文章的图文视频智能转载到你的百家号然后用AI伪创作改写发表，一定概率上会影响你这些账号的权重，考虑到这个问题作为一名程序员来说反复研究看了几遍百度这个是如何做的大致了解，利用业余时间制作了一版通用版图文生成视频的内容分享给大家。</p> 
<p>如果对教程不感兴趣的童鞋，可以直接关注我后查看我的视频里的内容，全都是基于数据技术自动化生成的短视频内容。</p> 
<p>好了，言归正传。</p> 
<p>先来看一下整体的业务流程目录，让大家大致有个了解。</p> 
<p><img alt="" src="https://img-blog.csdnimg.cn/img_convert/5f82ad0b4ad851da3fc92be4bec78bc0.png"></p> 
<p>具体操作流程如上，基于是python的技术，由于是通用简单版本，所以会比较单调，仅仅是实现了功能。比如特效、转场这些会在未来更新。</p> 
<p>&nbsp;</p> 
<p><strong>作品展示：</strong></p> 
<p><strong><a href="https://www.zhihu.com/zvideo/1290238134337892352">知乎上传作品《可爱日本萌妹たかきしおり「小巧脸蛋超清纯」》</a></strong></p> 
<p><strong><a href="https://haokan.baidu.com/v?pd=bjh&amp;vid=15263717994914941680&amp;fr=bjhauthor&amp;type=video">百家号上传作品《人气直播主饶方晴气质笑颜无害又迷人》</a></strong></p> 
<p>&nbsp;</p> 
<p>好了言归正传，具体业务讲解如下。</p> 
<p>记录抓取过的内容数据</p> 
<p>把自己抓取过的内容进行一个自动化记录，方便未来避免处理重复的内容。</p> 
<p><img alt="" src="https://img-blog.csdnimg.cn/img_convert/cecd167150a5e3b8a5140e6155579ba0.png"></p> 
<h2><a name="t0"></a><a name="t0"></a>&nbsp;</h2> 
<p>抓取文章的正文、标题、图片链接</p> 
<p>这里使用的是Python的requests方法抓取到你设置目标的文章的正文内容以及图片信息，为了让生成的视频不单调，建议多找些图片多的文章，或者在其中自己补充一些相关的图片，由于百度AI图文自动生成功能，他自身有强大的图片、视频数据库所以比相对局限的自制的内容就差一些，所以将就一下把。</p> 
<p>目前制作了的平台数据采集脚本不多，未来会更新。</p> 
<p><img alt="" src="https://img-blog.csdnimg.cn/img_convert/ebd72633df311c9a8d7cdcc278543f29.png"></p> 
<p>看一下抓取的结果，为了避免视频审核不通过，这里的Title和正文内容自己要修正一下，图片也要看好了避免一些不必要的麻烦，这里还可以进行一个去水印处理，使用opencv方法就可以了。</p> 
<p><img alt="" src="https://img-blog.csdnimg.cn/img_convert/0f86b46f8b2830d21e3f008d52d688c3.png"></p> 
<p>抓取的图片在这里可以看到。</p> 
<h2><a name="t1"></a><a name="t1"></a>&nbsp;</h2> 
<p>音频和字幕处理</p> 
<p>这里的思路大致是这样，比如你文章里有100个字先要用API接口的方式将这字幕转换成MP3文件作为解说音频，然后将字幕进行切分，这种切分方式我设置的一次显示20个作为字幕，然后进行循环切换。接下来记录MP3的时长。</p> 
<p><img alt="" src="https://img-blog.csdnimg.cn/img_convert/6b6678a269b9948a0e4fe2fcb09fe2bf.png"></p> 
<h2><a name="t2"></a><a name="t2"></a>&nbsp;</h2> 
<p>图片进行裁剪处理</p> 
<p>由于互联网文章里的图片尺寸不一样，所以我们要根据一定规则进行裁剪，这种裁剪方式根据你的模板进行设置，比如你做的事横板视频，竖版图片高度比不能超过你设置的横板尺寸。反之竖版图片也是同样的方式进行处理。这样就不会出现图片出现在视频中很别扭的情况了。</p> 
<p><img alt="" src="https://img-blog.csdnimg.cn/img_convert/b9f55418e040b8c704fbd6c2c8f4ab58.png"></p> 
<p>处理完的结果是这样</p> 
<p><img alt="" src="https://img-blog.csdnimg.cn/img_convert/2426fa0393cda0226b2dd230565b1c1b.png"></p> 
<h2><a name="t3"></a><a name="t3"></a>&nbsp;</h2> 
<p>选择一个抠图封面人物图像PNG</p> 
<p>做我们视频的封面，因为有的视频网站不能自定义视频封面的情况下是以第一帧作为视频封面的，所以我们要做一个，省去很多自定义的麻烦。</p> 
<p><img alt="" src="https://img-blog.csdnimg.cn/img_convert/ef6a8269dedbe5166e39e27ee81cec8d.png"></p> 
<p>然后将生成的png图片放到我们的封面图片中，这里我不会PS 就用PPT代替了</p> 
<p><img alt="" src="https://img-blog.csdnimg.cn/img_convert/718845a42bd05bc7f50e9ab347466c74.png"></p> 
<p>然后将这个封面的图片保存下来就可以了。</p> 
<p><img alt="" src="https://img-blog.csdnimg.cn/img_convert/485f230afe4b7e9a8f404fe5665572d2.png"></p> 
<h2><a name="t4"></a><a name="t4"></a>&nbsp;</h2> 
<p>素材都准备好了就开始合成咯</p> 
<ul><li> <p>将素材图片按照顺序进行切换与base.mp4进行合成。</p> </li></ul>
<p><img alt="" src="https://img-blog.csdnimg.cn/img_convert/8963351b8c5fdc5ab6a703e5b065b441.png"></p> 
<p><img alt="" src="https://img-blog.csdnimg.cn/img_convert/9be5529bd42799610a2fcf3340c5567b.png"></p> 
<ul><li> <p>将字幕按照顺序与上面生成的视频进行合成，在根据字幕的播放顺序进行匹对即可。</p> </li></ul>
<p><img alt="" src="https://img-blog.csdnimg.cn/img_convert/55e5f7b4468deef7ece9553f09950b6e.png"></p> 
<p><img alt="" src="https://img-blog.csdnimg.cn/img_convert/54859295fe0a33e093a6248ec44a7fef.png"></p> 
<ul><li> <p>将制作好的封面生成1秒不到的视频进行后续合成用顺便把title字幕也加进去。</p> </li></ul>
<p><img alt="" src="https://img-blog.csdnimg.cn/img_convert/e23c763195ec47dedb9c996e434fd063.png"></p> 
<p><img alt="" src="https://img-blog.csdnimg.cn/img_convert/506ae1f676348be77380d2bdeeca9fe3.png"></p> 
<ul><li> <p>拼接整个素材</p> </li></ul>
<p>这里准备好预先自己做好的开篇介绍和结尾推广的视频，如果没有也无所谓。</p> 
<p><img alt="" src="https://img-blog.csdnimg.cn/img_convert/d612680a5fd9996b1dc23a3b38b0371b.png"></p> 
<p><img alt="" src="https://img-blog.csdnimg.cn/img_convert/75ae8e353106cdd6b7d54696dcba4877.png"></p> 
<ul><li> <p>这里所有生成的素材有这些。</p> </li></ul>
<p><img alt="" src="https://img-blog.csdnimg.cn/img_convert/05f3bb76c94c7082272301c96c5159ac.png"></p> 
<ul><li> <p>最后把logo水印合成上去吧。</p> </li></ul>
<p><img alt="" src="https://img-blog.csdnimg.cn/img_convert/83cd500f2920b6b91e038d3ce86323c5.png"></p> 
<p>OK 最后大功告成，完成了一键生成视频的操作。</p> 
<p>可以关注一波然后点我的主页去查看各种技术流生成的视频啦。</p>
                </div>
