package com.kimiclaw.cameraassistant;

import android.accessibilityservice.AccessibilityServiceInfo;
import android.app.AlertDialog;
import android.content.Context;
import android.content.Intent;
import android.net.Uri;
import android.os.Bundle;
import android.provider.Settings;
import android.view.accessibility.AccessibilityManager;
import android.widget.Button;
import android.widget.TextView;
import android.widget.Toast;

import androidx.appcompat.app.AppCompatActivity;

import java.util.List;

public class MainActivity extends AppCompatActivity {

    private TextView tvStatus;
    private Button btnEnableService;
    private Button btnOpenSettings;
    private Button btnQuickTest;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        tvStatus = findViewById(R.id.tv_status);
        btnEnableService = findViewById(R.id.btn_enable_service);
        btnOpenSettings = findViewById(R.id.btn_open_settings);
        btnQuickTest = findViewById(R.id.btn_quick_test);

        btnEnableService.setOnClickListener(v -> openAccessibilitySettings());
        btnOpenSettings.setOnClickListener(v -> openOverlaySettings());
        btnQuickTest.setOnClickListener(v -> showQuickTips());

        updateServiceStatus();
    }

    @Override
    protected void onResume() {
        super.onResume();
        updateServiceStatus();
    }

    private void updateServiceStatus() {
        boolean isEnabled = isAccessibilityServiceEnabled();
        boolean hasOverlay = Settings.canDrawOverlays(this);

        if (isEnabled && hasOverlay) {
            tvStatus.setText("✅ 服务运行中\n打开相机时将自动显示拍摄指导");
            tvStatus.setTextColor(getResources().getColor(android.R.color.holo_green_dark));
            btnEnableService.setText("重新配置");
        } else {
            StringBuilder sb = new StringBuilder("⚠️ 服务未完全启用\n\n");
            if (!isEnabled) sb.append("• 无障碍权限未开启\n");
            if (!hasOverlay) sb.append("• 悬浮窗权限未开启\n");
            sb.append("\n请完成以下配置:");
            
            tvStatus.setText(sb.toString());
            tvStatus.setTextColor(getResources().getColor(android.R.color.holo_orange_dark));
            btnEnableService.setText("1. 开启无障碍权限");
        }

        if (!hasOverlay) {
            btnOpenSettings.setVisibility(android.view.View.VISIBLE);
        } else {
            btnOpenSettings.setVisibility(android.view.View.GONE);
        }
    }

    private boolean isAccessibilityServiceEnabled() {
        AccessibilityManager am = (AccessibilityManager) getSystemService(Context.ACCESSIBILITY_SERVICE);
        List<AccessibilityServiceInfo> enabledServices = am.getEnabledAccessibilityServiceList(
            AccessibilityServiceInfo.FEEDBACK_ALL_MASK
        );
        
        String serviceName = getPackageName() + "/" + CameraAccessibilityService.class.getName();
        
        for (AccessibilityServiceInfo service : enabledServices) {
            if (service.getId().equals(serviceName)) {
                return true;
            }
        }
        return false;
    }

    private void openAccessibilitySettings() {
        Intent intent = new Intent(Settings.ACTION_ACCESSIBILITY_SETTINGS);
        startActivity(intent);
        Toast.makeText(this, "找到「小米13U摄影助手」并开启", Toast.LENGTH_LONG).show();
    }

    private void openOverlaySettings() {
        if (!Settings.canDrawOverlays(this)) {
            Intent intent = new Intent(Settings.ACTION_MANAGE_OVERLAY_PERMISSION,
                Uri.parse("package:" + getPackageName()));
            startActivity(intent);
        }
    }

    private void showQuickTips() {
        new AlertDialog.Builder(this)
            .setTitle("⚡ 快速拍摄技巧")
            .setMessage(
                "街拍模式:\n" +
                "• 锁屏双击音量下键，0.8秒抓拍\n\n" +
                "可变光圈:\n" +
                "• f/1.9 = 最大虚化（人像）\n" +
                "• f/4.0 = 最佳画质（风景）\n\n" +
                "万能夜景:\n" +
                "• ISO 100 + 快门 2-30秒 + 三脚架\n\n" +
                "人像虚化:\n" +
                "• 75mm长焦 + f/1.9 + 距离1.5米\n\n" +
                "徕卡色彩:\n" +
                "• 画面中加入红/黄/蓝色更出片"
            )
            .setPositiveButton("知道了", null)
            .show();
    }
}
