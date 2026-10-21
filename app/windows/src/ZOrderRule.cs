namespace CrossPet
{
    static class ZOrderRule
    {
        /// <summary>桌面、任务栏（全屏判断也排除它们）</summary>
        public static bool IsShell(string cls) =>
            cls == "Progman" || cls == "WorkerW" || cls == "Shell_TrayWnd" || cls == "Shell_SecondaryTrayWnd";

        /// <summary>取消置顶时要不要插到前台窗口正下方（这样不会盖住你正在用的程序）。
        /// 只对普通程序窗口这么做：前台是桌面时插到它下面，桌宠就被壁纸整个盖住、哪里都找不到（1.3.7 用户反馈：
        /// 「跟着 AI」层级下右键几次、换个角色她就不见了，托盘和进程都还在）；前台是 CrossPet 自己的右键菜单、设置窗口时也不插</summary>
        public static bool TuckBelow(string frontClass, bool frontIsOurs) =>
            !frontIsOurs && !string.IsNullOrEmpty(frontClass) && !IsShell(frontClass);
    }
}
