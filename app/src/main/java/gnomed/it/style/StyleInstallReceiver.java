package gnomed.it.style;

import android.content.BroadcastReceiver;
import android.content.Context;
import android.content.Intent;
import android.content.pm.PackageInstaller;
import android.widget.Toast;

import gnomed.it.R;

/** Result of the style update session: asks the user to confirm, or reports a failure. */
public class StyleInstallReceiver extends BroadcastReceiver {

    @Override
    @SuppressWarnings("deprecation")
    public void onReceive(Context context, Intent intent) {
        int status = intent.getIntExtra(PackageInstaller.EXTRA_STATUS, PackageInstaller.STATUS_FAILURE);
        if (status == PackageInstaller.STATUS_PENDING_USER_ACTION) {
            Intent confirm = intent.getParcelableExtra(Intent.EXTRA_INTENT);
            if (confirm != null) {
                confirm.addFlags(Intent.FLAG_ACTIVITY_NEW_TASK);
                context.startActivity(confirm);
            }
        } else if (status != PackageInstaller.STATUS_SUCCESS) {
            String msg = intent.getStringExtra(PackageInstaller.EXTRA_STATUS_MESSAGE);
            if (status == PackageInstaller.STATUS_FAILURE_CONFLICT
                    || status == PackageInstaller.STATUS_FAILURE_INCOMPATIBLE) {
                msg = context.getString(R.string.gnomed_style_signature);
            }
            Toast.makeText(context, context.getString(R.string.gnomed_style_failed, msg), Toast.LENGTH_LONG).show();
        }
    }
}
