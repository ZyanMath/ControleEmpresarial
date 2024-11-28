import com.journeyapps.barcodescanner.BarcodeEncoder;
import com.journeyapps.barcodescanner.BarcodeCallback;
import com.journeyapps.barcodescanner.CaptureActivity;

public class QRCodeScannerActivity extends CaptureActivity {
    // Inicialização do scanner
    private void startScanning() {
        BarcodeEncoder barcodeEncoder = new BarcodeEncoder();
        barcodeEncoder.setBarcodeCallback(new BarcodeCallback() {
            @Override
            public void barcodeResult(BarcodeResult result) {
                // Processar o resultado do QR code
                String userId = result.getText();
                // Registrar presença no banco de dados
                registerPresence(userId);
            }
        });
    }
}