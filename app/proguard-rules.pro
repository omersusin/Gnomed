-optimizationpasses 5
-overloadaggressively
-dontpreverify
-repackageclasses 'o'
-allowaccessmodification

-keep class **.R
-keep class **.R$* {
    <fields>;
}

# Keep the source line when using ProGuard
-keepattributes SourceFile,LineNumberTable
-renamesourcefileattribute SourceFile

# --- Gnomed ---
# CandyBar uses WorkManager, whose Room database (WorkDatabase_Impl) is created by
# reflection through its no-arg constructor. R8 removed that constructor in the
# release build -> "NoSuchMethodException: WorkDatabase_Impl.<init>" crash at startup.
-keep class * extends androidx.room.RoomDatabase { <init>(); }
-keep class androidx.work.impl.WorkDatabase_Impl { *; }
# Workers are instantiated by class name with (Context, WorkerParameters).
-keep class * extends androidx.work.ListenableWorker {
    public <init>(android.content.Context, androidx.work.WorkerParameters);
}
