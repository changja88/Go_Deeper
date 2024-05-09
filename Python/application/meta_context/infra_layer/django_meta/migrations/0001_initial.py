# Generated by Django 5.0.3 on 2024-04-11 15:12

import applications.common.enum
import applications.member.domain_layer.value_object.enum
import application.meta_context.domain_layer.meta_enum
import application.meta_context.infra_layer.django_meta.models.certification_orm
import application.meta_context.infra_layer.django_meta.models.member_photo_orm
import django.db.models.deletion
import django.utils.timezone
import django_extensions.db.fields
import model_utils.fields
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="CertificationORM",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                (
                    "created",
                    django_extensions.db.fields.CreationDateTimeField(auto_now_add=True, verbose_name="created"),
                ),
                (
                    "modified",
                    django_extensions.db.fields.ModificationDateTimeField(auto_now=True, verbose_name="modified"),
                ),
                (
                    "censor_status",
                    models.CharField(
                        choices=[
                            (application.meta_context.domain_layer.meta_enum.CensorStatus["UNDER_CENSOR"], "심사중"),
                            (application.meta_context.domain_layer.meta_enum.CensorStatus["APPROVED"], "심사 완료"),
                            (application.meta_context.domain_layer.meta_enum.CensorStatus["REJECTED"], "심사 거절"),
                        ],
                        db_index=True,
                        default=application.meta_context.domain_layer.meta_enum.CensorStatus["UNDER_CENSOR"],
                        verbose_name="심사 결과",
                    ),
                ),
                ("rejected_reason", models.CharField(default=None, null=True, verbose_name="검열 실패 이유")),
            ],
            options={
                "verbose_name": "[certification] 사용자 신체 메타 정보",
                "verbose_name_plural": "[certification] 사용자 신체 메타 정보",
                "db_table": "certification",
            },
        ),
        migrations.CreateModel(
            name="DateTestMetaQuestionPresetORM",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("question", models.CharField(verbose_name="연애고사 질문")),
                ("type", models.CharField(verbose_name="연애고사 질문 타입")),
                ("order", models.PositiveIntegerField(verbose_name="질문 순서")),
            ],
            options={
                "verbose_name": "[date_test_meta_question] 연애 고사 질문지",
                "verbose_name_plural": "[date_test_meta_question] 연애 고사 질문지",
                "db_table": "date_test_meta_question",
            },
        ),
        migrations.CreateModel(
            name="EducationMetaPresetORM",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("value", models.CharField(verbose_name="학교명")),
                (
                    "type",
                    models.CharField(
                        choices=[
                            (application.meta_context.domain_layer.meta_enum.UniversityType["DOMESTIC"], "국내 대학"),
                            (
                                application.meta_context.domain_layer.meta_enum.UniversityType["INTERNATIONAL"],
                                "해외 대학",
                            ),
                        ],
                        db_index=True,
                        verbose_name="타입",
                    ),
                ),
                ("is_show", models.CharField(default=True, verbose_name="사용자 직접입력 값 승인여부")),
                ("tear", models.PositiveSmallIntegerField(default=0, help_text="평가 티어")),
            ],
            options={
                "verbose_name": "[education_meta_preset] 학력 정보 선택지",
                "verbose_name_plural": "[education_meta_preset] 학력 정보 선택지",
                "db_table": "education_meta_preset",
            },
        ),
        migrations.CreateModel(
            name="FinanceMetaPresetORM",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("value", models.CharField(verbose_name="경제력 메타 값")),
                (
                    "type",
                    models.CharField(
                        choices=[
                            (application.meta_context.domain_layer.meta_enum.FinanceMetaType["JOB"], "직업"),
                            (application.meta_context.domain_layer.meta_enum.FinanceMetaType["INCOME"], "소득"),
                            (application.meta_context.domain_layer.meta_enum.FinanceMetaType["COMPANY"], "회사"),
                            (application.meta_context.domain_layer.meta_enum.FinanceMetaType["ASSET"], "자산"),
                            (
                                application.meta_context.domain_layer.meta_enum.FinanceMetaType["FAMILY_ASSET"],
                                "집안 자산",
                            ),
                            (
                                application.meta_context.domain_layer.meta_enum.FinanceMetaType["CAR_BRAND"],
                                "차량 브랜드",
                            ),
                            (application.meta_context.domain_layer.meta_enum.FinanceMetaType["CAR_PRICE"], "차량 가격"),
                            (application.meta_context.domain_layer.meta_enum.FinanceMetaType["MOTHER_JOB"], "모 직업"),
                            (application.meta_context.domain_layer.meta_enum.FinanceMetaType["FATHER_JOB"], "부 직업"),
                        ],
                        db_index=True,
                        verbose_name="타입",
                    ),
                ),
                ("is_show", models.CharField(default=True, verbose_name="사용자 직접입력 값 승인여부")),
                ("tear", models.PositiveSmallIntegerField(default=0, help_text="평가 티어")),
            ],
            options={
                "verbose_name": "[finance_meta_preset] 경제력 정보 선택지",
                "verbose_name_plural": "[finance_meta_preset] 경제력 정보 선택지",
                "db_table": "finance_meta_preset",
            },
        ),
        migrations.CreateModel(
            name="MemberPhotoORM",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                (
                    "created",
                    model_utils.fields.AutoCreatedField(
                        default=django.utils.timezone.now, editable=False, verbose_name="created"
                    ),
                ),
                (
                    "modified",
                    model_utils.fields.AutoLastModifiedField(
                        default=django.utils.timezone.now, editable=False, verbose_name="modified"
                    ),
                ),
                ("member_id", models.PositiveBigIntegerField(db_index=True)),
                (
                    "file",
                    models.ImageField(
                        upload_to=application.meta_context.infra_layer.django_meta.models.member_photo_orm.get_s3_file_path
                    ),
                ),
                (
                    "type",
                    models.CharField(
                        choices=[
                            (application.meta_context.domain_layer.meta_enum.PhotoType["FACE"], "얼굴 사진"),
                            (application.meta_context.domain_layer.meta_enum.PhotoType["ETC"], "기타 사진"),
                        ],
                        verbose_name="사진 타입",
                    ),
                ),
                (
                    "censor_status",
                    models.CharField(
                        choices=[
                            (application.meta_context.domain_layer.meta_enum.CensorStatus["APPROVED"], "인증 완료"),
                            (application.meta_context.domain_layer.meta_enum.CensorStatus["REJECTED"], "인증 불가"),
                            (application.meta_context.domain_layer.meta_enum.CensorStatus["UNDER_CENSOR"], "심사 중"),
                        ],
                        verbose_name="검열 상태",
                    ),
                ),
                ("is_main", models.BooleanField(default=False, verbose_name="대표 사진 여부")),
                ("is_deleted", models.BooleanField(default=False, verbose_name="사진 삭제 여부")),
                ("rejected_reason", models.CharField(default=None, null=True, verbose_name="검열 실패 이유")),
            ],
            options={
                "verbose_name": "[member_photo] 멤버 사진 정보",
                "verbose_name_plural": "[member_photo] 멤버 사진 정보",
                "db_table": "member_photo",
            },
        ),
        migrations.CreateModel(
            name="PhysicalMetaPresetORM",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("value", models.CharField(verbose_name="타입에 해당하는 값")),
                (
                    "type",
                    models.CharField(
                        choices=[
                            (application.meta_context.domain_layer.meta_enum.PhysicalMetaType["BODY_SHAPE"], "체형"),
                            (application.meta_context.domain_layer.meta_enum.PhysicalMetaType["HEIGHT"], "체중"),
                            (application.meta_context.domain_layer.meta_enum.PhysicalMetaType["WEIGHT"], "키"),
                        ],
                        db_index=True,
                        verbose_name="타입",
                    ),
                ),
            ],
            options={
                "verbose_name": "[physical_meta_preset] 신체 정보 선택지",
                "verbose_name_plural": "[physical_meta_preset] 신체 정보 선택지",
                "db_table": "physical_meta_preset",
            },
        ),
        migrations.CreateModel(
            name="PreferenceMetaPresetORM",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                (
                    "type",
                    models.CharField(
                        choices=[
                            (application.meta_context.domain_layer.meta_enum.PreferenceMetaType["SMOKING"], "흡연"),
                            (application.meta_context.domain_layer.meta_enum.PreferenceMetaType["ALCOHOL"], "음주"),
                            (application.meta_context.domain_layer.meta_enum.PreferenceMetaType["HOBBY"], "취미"),
                            (application.meta_context.domain_layer.meta_enum.PreferenceMetaType["RELIGION"], "종교"),
                            (
                                application.meta_context.domain_layer.meta_enum.PreferenceMetaType["DATE_STYLE"],
                                "데이트 스타일",
                            ),
                            (application.meta_context.domain_layer.meta_enum.PreferenceMetaType["MBTI"], "MBTI"),
                        ],
                        db_index=True,
                        verbose_name="타입",
                    ),
                ),
                ("value", models.CharField(default=None, null=True, verbose_name="마지막 값")),
            ],
            options={
                "verbose_name": "[preference_meta_preset] 기호 정보 선택지",
                "verbose_name_plural": "[preference_meta_preset] 기호 정보 선택지",
                "db_table": "preference_meta_preset",
            },
        ),
        migrations.CreateModel(
            name="CertificationFileORM",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                (
                    "created",
                    django_extensions.db.fields.CreationDateTimeField(auto_now_add=True, verbose_name="created"),
                ),
                (
                    "modified",
                    django_extensions.db.fields.ModificationDateTimeField(auto_now=True, verbose_name="modified"),
                ),
                (
                    "file",
                    models.FileField(
                        upload_to=application.meta_context.infra_layer.django_meta.models.certification_orm.get_s3_cerification_file_path
                    ),
                ),
                ("is_deleted", models.BooleanField(default=False)),
                (
                    "certification",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="certification_file",
                        to="django_meta.certificationorm",
                    ),
                ),
            ],
            options={
                "verbose_name": "[certification_file] 멤버 메타 인증",
                "verbose_name_plural": "[certification_file] 멤버 메타 인증",
                "db_table": "certification_file",
            },
        ),
        migrations.CreateModel(
            name="DateTestMetaAnswerPresetORM",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("answer", models.CharField(verbose_name="연애고사 답변")),
                ("order", models.PositiveIntegerField(verbose_name="표기 순서")),
                (
                    "question",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="answer",
                        to="django_meta.datetestmetaquestionpresetorm",
                    ),
                ),
            ],
            options={
                "verbose_name": "[date_test_meta_answer] 연애 고사 답변",
                "verbose_name_plural": "[date_test_meta_answer] 연애 고사 답변",
                "db_table": "date_test_meta_answer",
            },
        ),
        migrations.CreateModel(
            name="MemberBirthMetaORM",
            fields=[
                (
                    "created",
                    django_extensions.db.fields.CreationDateTimeField(auto_now_add=True, verbose_name="created"),
                ),
                (
                    "modified",
                    django_extensions.db.fields.ModificationDateTimeField(auto_now=True, verbose_name="modified"),
                ),
                ("id", models.AutoField(primary_key=True, serialize=False)),
                ("birth_year", models.PositiveIntegerField()),
                (
                    "gender",
                    models.CharField(
                        choices=[
                            (applications.common.enum.Gender["FEMALE"], "여자"),
                            (applications.common.enum.Gender["MALE"], "남자"),
                        ],
                        verbose_name="성별",
                    ),
                ),
                (
                    "member",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="birth_meta",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "verbose_name": "[member_birth_meta] 사용자 출생 메타 정보",
                "verbose_name_plural": "[member_birth_meta] 사용자 출생 메타 정보",
                "db_table": "member_birth_meta",
            },
        ),
        migrations.CreateModel(
            name="MemberDateTestMetaORM",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                (
                    "created",
                    django_extensions.db.fields.CreationDateTimeField(auto_now_add=True, verbose_name="created"),
                ),
                (
                    "modified",
                    django_extensions.db.fields.ModificationDateTimeField(auto_now=True, verbose_name="modified"),
                ),
                (
                    "answer",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="django_meta.datetestmetaanswerpresetorm"
                    ),
                ),
                ("member", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                (
                    "question",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="django_meta.datetestmetaquestionpresetorm"
                    ),
                ),
            ],
            options={
                "verbose_name": "[member_date_test_meta] 멤버 연애 고사 답변",
                "verbose_name_plural": "[member_date_test_meta] 멤버 연애 고사 답변",
                "db_table": "member_date_test_meta",
            },
        ),
        migrations.CreateModel(
            name="MemberPhotoVisibilityORM",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                (
                    "created",
                    model_utils.fields.AutoCreatedField(
                        default=django.utils.timezone.now, editable=False, verbose_name="created"
                    ),
                ),
                (
                    "modified",
                    model_utils.fields.AutoLastModifiedField(
                        default=django.utils.timezone.now, editable=False, verbose_name="modified"
                    ),
                ),
                (
                    "visibility",
                    models.CharField(
                        choices=[
                            (
                                applications.member.domain_layer.value_object.enum.PhotoVisibilityStatus[
                                    "PUBLIC"
                                ],
                                "공개",
                            ),
                            (
                                applications.member.domain_layer.value_object.enum.PhotoVisibilityStatus[
                                    "PRIVATE"
                                ],
                                "비공개",
                            ),
                        ],
                        default=applications.member.domain_layer.value_object.enum.PhotoVisibilityStatus[
                            "PUBLIC"
                        ],
                        verbose_name="사진 공개여부",
                    ),
                ),
                (
                    "member",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="photo_visibility",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "verbose_name": "[member_photo_visibility] 멤버 사진 공개 여부",
                "verbose_name_plural": "[member_photo_visibility] 멤버 사진 공개 여부",
                "db_table": "member_photo_visibility",
            },
        ),
        migrations.CreateModel(
            name="MemberPhysicalMetaORM",
            fields=[
                (
                    "created",
                    django_extensions.db.fields.CreationDateTimeField(auto_now_add=True, verbose_name="created"),
                ),
                (
                    "modified",
                    django_extensions.db.fields.ModificationDateTimeField(auto_now=True, verbose_name="modified"),
                ),
                ("id", models.AutoField(primary_key=True, serialize=False)),
                (
                    "member",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="physical_meta",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "physical_meta",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="member_physical_meta",
                        to="django_meta.physicalmetapresetorm",
                    ),
                ),
            ],
            options={
                "verbose_name": "[member_physical_meta] 사용자 신체 메타 정보",
                "verbose_name_plural": "[member_physical_meta] 사용자 신체 메타 정보",
                "db_table": "member_physical_meta",
            },
        ),
        migrations.CreateModel(
            name="MemberPreferenceMetaORM",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                (
                    "created",
                    django_extensions.db.fields.CreationDateTimeField(auto_now_add=True, verbose_name="created"),
                ),
                (
                    "modified",
                    django_extensions.db.fields.ModificationDateTimeField(auto_now=True, verbose_name="modified"),
                ),
                ("member_id", models.PositiveIntegerField(db_index=True)),
                (
                    "preference_meta",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="member_preference_meta",
                        to="django_meta.preferencemetapresetorm",
                    ),
                ),
            ],
            options={
                "verbose_name": "[member_preference_meta] 사용자 기호 정보",
                "verbose_name_plural": "[member_preference_meta] 사용자 기호 정보",
                "db_table": "member_preference_meta",
            },
        ),
        migrations.CreateModel(
            name="MemberEducationMetaORM",
            fields=[
                (
                    "certificationorm_ptr",
                    models.OneToOneField(
                        auto_created=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        parent_link=True,
                        primary_key=True,
                        serialize=False,
                        to="django_meta.certificationorm",
                    ),
                ),
                ("member_id", models.PositiveIntegerField(db_index=True)),
                (
                    "education_meta",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="member_education_meta",
                        to="django_meta.educationmetapresetorm",
                    ),
                ),
            ],
            options={
                "verbose_name": "[member_education_meta] 사용자 학력 정보",
                "verbose_name_plural": "[member_education_meta] 사용자 학력 계정",
                "db_table": "member_education_meta",
            },
            bases=("django_meta.certificationorm",),
        ),
        migrations.CreateModel(
            name="MemberFinanceMetaORM",
            fields=[
                (
                    "certificationorm_ptr",
                    models.OneToOneField(
                        auto_created=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        parent_link=True,
                        primary_key=True,
                        serialize=False,
                        to="django_meta.certificationorm",
                    ),
                ),
                ("member_id", models.PositiveIntegerField(db_index=True)),
                (
                    "finance_meta",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="member_finance_meta",
                        to="django_meta.financemetapresetorm",
                    ),
                ),
            ],
            options={
                "verbose_name": "[member_finance_meta] 사용자 경제력 정보",
                "verbose_name_plural": "[member_finance_meta] 사용자 경제력 계정",
                "db_table": "member_finance_meta",
            },
            bases=("django_meta.certificationorm",),
        ),
        migrations.AddConstraint(
            model_name="memberdatetestmetaorm",
            constraint=models.UniqueConstraint(
                fields=("member", "question", "answer"), name="member_date_test_result_unique"
            ),
        ),
    ]
