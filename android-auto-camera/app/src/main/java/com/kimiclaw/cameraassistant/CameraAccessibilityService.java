// CameraAccessibilityService.java
// Android无障碍服务 - 自动检测相机启动并显示拍摄建议

package com.kimiclaw.cameraassistant;

import android.accessibilityservice.AccessibilityService;
import android.accessibilityservice.AccessibilityServiceInfo;
import android.app.Notification;
import android.app.NotificationChannel;
import android.app.NotificationManager;
import android.app.PendingIntent;
import android.content.Context;
import android.content.Intent;
import android.graphics.PixelFormat;
import android.os.Build;
import android.os.Handler;
import android.os.Looper;
import android.view.Gravity;
import android.view.LayoutInflater;
import android.view.View;
import android.view.WindowManager;
import android.view.accessibility.AccessibilityEvent;
import android.widget.Button;
import android.widget.LinearLayout;
import android.widget.TextView;
import android.widget.Toast;

import androidx.core.app.NotificationCompat;

public class CameraAccessibilityService extends AccessibilityService {
    
    private static final String[] CAMERA_PACKAGES = {
        "com.android.camera",
        "com.miui.camera",
        "com.android.camera2",
        "com.xiaomi.camera",
        "com.google.android.GoogleCamera"
    };
    
    private WindowManager windowManager;
    private View floatingView;
    private boolean isShowingGuide = false;
    private Handler mainHandler = new Handler(Looper.getMainLooper());
    
    @Override
    public void onCreate() {
        super.onCreate();
        windowManager = (WindowManager) getSystemService(Context.WINDOW_SERVICE);
        createNotificationChannel();
        startForeground(1, createNotification());
    }
    
    @Override
    protected void onServiceConnected() {
        super.onServiceConnected();
        AccessibilityServiceInfo info = new AccessibilityServiceInfo();
        info.eventTypes = AccessibilityEvent.TYPE_WINDOW_STATE_CHANGED;
        info.feedbackType = AccessibilityServiceInfo.FEEDBACK_GENERIC;
        info.notificationTimeout = 100;
        setServiceInfo(info);
        
        Toast.makeText(this, "小米13U摄影助手已启动", Toast.LENGTH_SHORT).show();
    }
    
    @Override
    public void onAccessibilityEvent(AccessibilityEvent event) {
        if (event.getEventType() == AccessibilityEvent.TYPE_WINDOW_STATE_CHANGED) {
            CharSequence packageName = event.getPackageName();
            if (packageName != null) {
                String pkg = packageName.toString();
                
                for (String cameraPkg : CAMERA_PACKAGES) {
                    if (pkg.contains(cameraPkg)) {
                        showCameraGuide();
                        return;
                    }
                }
                
                // 相机关闭，隐藏指导
                if (isShowingGuide) {
                    hideCameraGuide();
                }
            }
        }
    }
    
    @Override
    public void onInterrupt() {
        // 服务中断
    }
    
    private void showCameraGuide() {
        if (isShowingGuide) return;
        
        mainHandler.post(() -> {
            try {
                WindowManager.LayoutParams params = new WindowManager.LayoutParams(
                    WindowManager.LayoutParams.MATCH_PARENT,
                    WindowManager.LayoutParams.WRAP_CONTENT,
                    Build.VERSION.SDK_INT >= Build.VERSION_CODES.O 
                        ? WindowManager.LayoutParams.TYPE_APPLICATION_OVERLAY
                        : WindowManager.LayoutParams.TYPE_PHONE,
                    WindowManager.LayoutParams.FLAG_NOT_FOCUSABLE 
                        | WindowManager.LayoutParams.FLAG_NOT_TOUCH_MODAL,
                    PixelFormat.TRANSLUCENT
                );
                params.gravity = Gravity.TOP;
                
                // 加载布局
                LayoutInflater inflater = LayoutInflater.from(this);
                floatingView = inflater.inflate(R.layout.camera_guide_overlay, null);
                
                // 设置场景按钮
                setupSceneButtons(floatingView);
                
                // 关闭按钮
                Button closeBtn = floatingView.findViewById(R.id.btn_close);
                closeBtn.setOnClickListener(v -> hideCameraGuide());
                
                // 最小化按钮
                Button minimizeBtn = floatingView.findViewById(R.id.btn_minimize);
                minimizeBtn.setOnClickListener(v -> minimizeGuide());
                
                windowManager.addView(floatingView, params);
                isShowingGuide = true;
                
            } catch (Exception e) {
                e.printStackTrace();
            }
        });
    }
    
    private void setupSceneButtons(View view) {
        // 人像
        view.findViewById(R.id.btn_portrait).setOnClickListener(v -> {
            showSceneDetail("人像", "75mm长焦", "f/1.9", "ISO 100-400", "1/125s");
        });
        
        // 夜景
        view.findViewById(R.id.btn_night).setOnClickListener(v -> {
            showSceneDetail("夜景", "23mm主摄", "f/1.9", "ISO 50-200", "2-30s");
        });
        
        // 街拍
        view.findViewById(R.id.btn_street).setOnClickListener(v -> {
            showSceneDetail("街拍", "23mm主摄", "f/4.0", "自动", "1/250s");
            Toast.makeText(this, "街拍快捷键: 锁屏双击音量下", Toast.LENGTH_LONG).show();
        });
        
        // 风景
        view.findViewById(R.id.btn_landscape).setOnClickListener(v -> {
            showSceneDetail("风景", "12mm超广", "f/4.0", "ISO 50-100", "自动");
        });
        
        // 美食
        view.findViewById(R.id.btn_food).setOnClickListener(v -> {
            showSceneDetail("美食", "75mm长焦", "f/1.9", "ISO 100-800", "1/60s");
        });
        
        // 星空
        view.findViewById(R.id.btn_star).setOnClickListener(v -> {
            showSceneDetail("星空", "23mm主摄", "f/1.9", "ISO 1600", "15-25s");
            Toast.makeText(this, "需要三脚架! 快门>15秒星星会拖线", Toast.LENGTH_LONG).show();
        });
        
        // 快速提示
        view.findViewById(R.id.btn_quick_tips).setOnClickListener(v -> {
            showQuickTips();
        });
    }
    
    private void showSceneDetail(String scene, String focal, String aperture, String iso, String shutter) {
        String message = String.format(
            "【%s】\n📷 %s | 🔆 %s\n⚙️ ISO %s | ⏱️ %s",
            scene, focal, aperture, iso, shutter
        );
        
        // 创建详细弹窗
        View detailView = LayoutInflater.from(this).inflate(R.layout.scene_detail_dialog, null);
        
        ((TextView) detailView.findViewById(R.id.tv_scene_name)).setText(scene);
        ((TextView) detailView.findViewById(R.id.tv_focal)).setText(focal);
        ((TextView) detailView.findViewById(R.id.tv_aperture)).setText(aperture);
        ((TextView) detailView.findViewById(R.id.tv_iso)).setText(iso);
        ((TextView) detailView.findViewById(R.id.tv_shutter)).setText(shutter);
        
        // 显示详细参数
        WindowManager.LayoutParams params = new WindowManager.LayoutParams(
            WindowManager.LayoutParams.WRAP_CONTENT,
            WindowManager.LayoutParams.WRAP_CONTENT,
            Build.VERSION.SDK_INT >= Build.VERSION_CODES.O 
                ? WindowManager.LayoutParams.TYPE_APPLICATION_OVERLAY
                : WindowManager.LayoutParams.TYPE_PHONE,
            WindowManager.LayoutParams.FLAG_NOT_FOCUSABLE,
            PixelFormat.TRANSLUCENT
        );
        params.gravity = Gravity.CENTER;
        
        try {
            windowManager.addView(detailView, params);
            
            // 5秒后自动关闭
            mainHandler.postDelayed(() -> {
                try {
                    windowManager.removeView(detailView);
                } catch (Exception e) {
                    e.printStackTrace();
                }
            }, 5000);
            
        } catch (Exception e) {
            e.printStackTrace();
            Toast.makeText(this, message, Toast.LENGTH_LONG).show();
        }
    }
    
    private void showQuickTips() {
        String tips = "⚡ 快速提示:\n" +
                "• 街拍: 锁屏双击音量下\n" +
                "• 可变光圈: f/1.9虚化 f/4.0画质\n" +
                "• 夜景: 必须上三脚架\n" +
                "• 人像: 75mm + 1.5米最佳\n" +
                "• 徕卡色: 加红黄蓝更出片";
        Toast.makeText(this, tips, Toast.LENGTH_LONG).show();
    }
    
    private void minimizeGuide() {
        if (floatingView != null) {
            // 最小化为小圆点
            View minimizedView = LayoutInflater.from(this).inflate(R.layout.minimized_guide, null);
            
            minimizedView.setOnClickListener(v -> {
                windowManager.removeView(minimizedView);
                showCameraGuide();
            });
            
            WindowManager.LayoutParams params = new WindowManager.LayoutParams(
                120, 120,
                Build.VERSION.SDK_INT >= Build.VERSION_CODES.O 
                    ? WindowManager.LayoutParams.TYPE_APPLICATION_OVERLAY
                    : WindowManager.LayoutParams.TYPE_PHONE,
                WindowManager.LayoutParams.FLAG_NOT_FOCUSABLE,
                PixelFormat.TRANSLUCENT
            );
            params.gravity = Gravity.TOP | Gravity.START;
            params.x = 50;
            params.y = 100;
            
            windowManager.removeView(floatingView);
            windowManager.addView(minimizedView, params);
            floatingView = minimizedView;
        }
    }
    
    private void hideCameraGuide() {
        if (floatingView != null && isShowingGuide) {
            try {
                windowManager.removeView(floatingView);
                floatingView = null;
                isShowingGuide = false;
            } catch (Exception e) {
                e.printStackTrace();
            }
        }
    }
    
    private void createNotificationChannel() {
        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.O) {
            NotificationChannel channel = new NotificationChannel(
                "camera_assistant",
                "相机助手服务",
                NotificationManager.IMPORTANCE_LOW
            );
            channel.setDescription("在后台检测相机启动");
            NotificationManager manager = getSystemService(NotificationManager.class);
            manager.createNotificationChannel(channel);
        }
    }
    
    private Notification createNotification() {
        Intent notificationIntent = new Intent(this, MainActivity.class);
        PendingIntent pendingIntent = PendingIntent.getActivity(
            this, 0, notificationIntent, 
            PendingIntent.FLAG_IMMUTABLE
        );
        
        return new NotificationCompat.Builder(this, "camera_assistant")
            .setContentTitle("小米13U摄影助手")
            .setContentText("正在监控相机启动...")
            .setSmallIcon(android.R.drawable.ic_menu_camera)
            .setContentIntent(pendingIntent)
            .build();
    }
    
    @Override
    public void onDestroy() {
        super.onDestroy();
        hideCameraGuide();
    }
}
