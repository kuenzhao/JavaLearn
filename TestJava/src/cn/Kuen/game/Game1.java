package cn.Kuen.game;
import com.rupeng.game.GameCore;;
public class Game1 implements Runnable{
	public static void main(String[] args)
	{
		GameCore.start(new Game1());
//		System.out.println("Hello World");
	}
	
	public void run()
	{
//		for(int i = 400;i <= 800;i += 100)
//		{
//			GameCore.setGameSize(i, i);//设置引擎的尺寸
//			GameCore.pause(2000);
//		}
		
//		GameCore.loadBgView("FD-242.JPG");//加载背景图片
//		GameCore.alert("Hello hahhahaahah");
//		GameCore.setGameTitle("kuen 的游戏引擎");
//		GameCore.pause(3000);
//		
//		GameCore.alert(555);
		
		
//		GameCore.setGameSize(300, 200);
//		GameCore.setGameTitle("kuen 的游戏引擎");
//		GameCore.pause(2000);
//		GameCore.setGameSize(400, 200);
//		GameCore.setGameTitle("哈哈哈，笑死我了");
//		GameCore.pause(2000);
		GameCore.alert("第一关");
		GameCore.playSound("超级玛丽民乐版.mp3", true);
		//GameCore.playSound("按键音2.mp3", false);
		GameCore.pause(5000);
		GameCore.closeSound("超级玛丽民乐版.mp3");
		GameCore.alert("第二关");
		GameCore.playSound("HOT.mp3", true);
		GameCore.pause(20000);
	}
}
